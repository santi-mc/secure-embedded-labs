#include "identity_service/identity_service.hpp"

#include "lab02_domain/identity_contract.hpp"
#include "lab02_domain/version.hpp"

#include "mbedtls/md.h"

#include <cstdio>

namespace secure_lab {

namespace {

inline constexpr std::size_t kDerivedDigestBytes = 12U;
inline constexpr std::size_t kMinInsecureDeviceIdLength = 3U;
inline constexpr std::size_t kMaxInsecureDeviceIdLength = 48U;

bool isVisibleAscii(const char c) noexcept
{
    return (static_cast<unsigned char>(c) >= 0x21U) &&
           (static_cast<unsigned char>(c) <= 0x7EU);
}

}  // namespace

IdentityService::IdentityService(const IDeviceUniqueSource& unique_source)
    : unique_source_(unique_source), insecure_device_id_(kInsecureSharedDeviceId)
{
}

IdentityView IdentityService::current(const SecurityProfile profile) const
{
    if (profile == SecurityProfile::Insecure) {
        return insecureView();
    }
    return hardenedView();
}

IdentityUpdateStatus IdentityService::setDeviceId(const std::string& device_id,
                                                  const SecurityProfile profile)
{
    if (profile != SecurityProfile::Insecure) {
        return IdentityUpdateStatus::RejectedByPolicy;
    }

    if (!isValidInsecureDeviceId(device_id)) {
        return IdentityUpdateStatus::RejectedInvalidValue;
    }

    insecure_device_id_ = device_id;
    return IdentityUpdateStatus::Accepted;
}

IdentityView IdentityService::insecureView() const
{
    const HardwareUniqueId hardware_id = unique_source_.readHardwareUniqueId();
    return IdentityView{insecure_device_id_,
                        "hardcoded_mutable_console_value",
                        toHex(hardware_id),
                        "true",
                        "true"};
}

IdentityView IdentityService::hardenedView() const
{
    const HardwareUniqueId hardware_id = unique_source_.readHardwareUniqueId();
    return IdentityView{derivePublicDeviceId(hardware_id),
                        "efuse_mac_sha256_truncated",
                        kRedactedValue,
                        "false",
                        "false"};
}

void IdentityService::logIdentityStatus(const JsonLog& log, const SecurityProfile profile) const
{
    const IdentityView view = current(profile);
    log.event("identity_status",
              {{"project", kProjectName},
               {"fw_version", kFirmwareVersion},
               {"lab", kLabId},
               {"profile", secure_lab::toString(profile)},
               {"device_id", view.device_id},
               {"identity_source", view.source},
               {"mutable_by_console", view.mutable_by_console},
               {"claim_contains_secret", view.claim_contains_secret}});
}

void IdentityService::logIdentity(const JsonLog& log, const SecurityProfile profile) const
{
    const IdentityView view = current(profile);
    log.event("identity_dump",
              {{"profile", secure_lab::toString(profile)},
               {"device_id", view.device_id},
               {"identity_source", view.source},
               {"raw_hardware_id", view.raw_hardware_id},
               {"mutable_by_console", view.mutable_by_console}});
}

void IdentityService::logClaim(const JsonLog& log, const SecurityProfile profile) const
{
    const IdentityView view = current(profile);
    if (profile == SecurityProfile::Insecure) {
        log.event("identity_claim",
                  {{"profile", secure_lab::toString(profile)},
                   {"device_id", view.device_id},
                   {"claim_type", "insecure_cloneable_claim"},
                   {"auth_token", kInsecureSharedToken},
                   {"warning", "intentional_lab_vulnerability"}});
        return;
    }

    log.event("identity_claim",
              {{"profile", secure_lab::toString(profile)},
               {"device_id", view.device_id},
               {"claim_type", "public_identity_claim"},
               {"auth_token", kNotApplicable},
               {"warning", "identity_is_not_authentication"}});
}

const char* IdentityService::toString(const IdentityUpdateStatus status) noexcept
{
    switch (status) {
    case IdentityUpdateStatus::Accepted:
        return "accepted";
    case IdentityUpdateStatus::RejectedByPolicy:
        return "rejected_by_policy";
    case IdentityUpdateStatus::RejectedInvalidValue:
        return "invalid_value";
    default:
        return "unknown";
    }
}

std::string IdentityService::toHex(const HardwareUniqueId& id)
{
    std::string output;
    output.reserve(id.size() * 2U);
    for (const std::uint8_t byte : id) {
        char chunk[3] = {};
        static_cast<void>(std::snprintf(chunk, sizeof(chunk), "%02X", byte));
        output += chunk;
    }
    return output;
}

std::string IdentityService::derivePublicDeviceId(const HardwareUniqueId& id)
{
    std::array<std::uint8_t, 32> digest{};
    const mbedtls_md_info_t* info = mbedtls_md_info_from_type(MBEDTLS_MD_SHA256);
    if (info == nullptr) {
        return "lab02-identity-error";
    }

    mbedtls_md_context_t ctx;
    mbedtls_md_init(&ctx);
    int rc = mbedtls_md_setup(&ctx, info, 0);
    if (rc == 0) {
        rc = mbedtls_md_starts(&ctx);
    }
    if (rc == 0) {
        rc = mbedtls_md_update(&ctx,
                               reinterpret_cast<const unsigned char*>(kIdentityDerivationDomain),
                               std::char_traits<char>::length(kIdentityDerivationDomain));
    }
    if (rc == 0) {
        const std::uint8_t separator = 0U;
        rc = mbedtls_md_update(&ctx, &separator, sizeof(separator));
    }
    if (rc == 0) {
        rc = mbedtls_md_update(&ctx, id.data(), id.size());
    }
    if (rc == 0) {
        rc = mbedtls_md_finish(&ctx, digest.data());
    }
    mbedtls_md_free(&ctx);

    if (rc != 0) {
        return "lab02-identity-error";
    }

    std::string out{kIdentityPrefix};
    out += firstHexBytes(digest, kDerivedDigestBytes);
    return out;
}

std::string IdentityService::firstHexBytes(const std::array<std::uint8_t, 32>& digest,
                                           const std::size_t bytes)
{
    std::string output;
    output.reserve(bytes * 2U);
    for (std::size_t i = 0U; i < bytes; ++i) {
        char chunk[3] = {};
        static_cast<void>(std::snprintf(chunk, sizeof(chunk), "%02x", digest[i]));
        output += chunk;
    }
    return output;
}

bool IdentityService::isValidInsecureDeviceId(const std::string& device_id) noexcept
{
    if ((device_id.size() < kMinInsecureDeviceIdLength) ||
        (device_id.size() > kMaxInsecureDeviceIdLength)) {
        return false;
    }

    for (const char c : device_id) {
        if (!isVisibleAscii(c)) {
            return false;
        }
    }
    return true;
}

}  // namespace secure_lab
