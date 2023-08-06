from typegraph import t
from box import Box
from typegraph.importers.base.importer import Import
from typegraph.runtimes.http import HTTPRuntime


def import_siteVerification() -> Import:
    siteVerification = HTTPRuntime("https://www.googleapis.com/")

    renames = {
        "ErrorResponse": "_siteVerification_1_ErrorResponse",
        "SiteVerificationWebResourceListResponseIn": "_siteVerification_2_SiteVerificationWebResourceListResponseIn",
        "SiteVerificationWebResourceListResponseOut": "_siteVerification_3_SiteVerificationWebResourceListResponseOut",
        "SiteVerificationWebResourceGettokenRequestIn": "_siteVerification_4_SiteVerificationWebResourceGettokenRequestIn",
        "SiteVerificationWebResourceGettokenRequestOut": "_siteVerification_5_SiteVerificationWebResourceGettokenRequestOut",
        "SiteVerificationWebResourceGettokenResponseIn": "_siteVerification_6_SiteVerificationWebResourceGettokenResponseIn",
        "SiteVerificationWebResourceGettokenResponseOut": "_siteVerification_7_SiteVerificationWebResourceGettokenResponseOut",
        "SiteVerificationWebResourceResourceIn": "_siteVerification_8_SiteVerificationWebResourceResourceIn",
        "SiteVerificationWebResourceResourceOut": "_siteVerification_9_SiteVerificationWebResourceResourceOut",
    }

    types = {}
    types["ErrorResponse"] = t.struct(
        {"code": t.integer(), "message": t.string(), "status": t.string()}
    ).named(renames["ErrorResponse"])
    types["SiteVerificationWebResourceListResponseIn"] = t.struct(
        {
            "items": t.array(
                t.proxy(renames["SiteVerificationWebResourceResourceIn"])
            ).optional()
        }
    ).named(renames["SiteVerificationWebResourceListResponseIn"])
    types["SiteVerificationWebResourceListResponseOut"] = t.struct(
        {
            "items": t.array(
                t.proxy(renames["SiteVerificationWebResourceResourceOut"])
            ).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["SiteVerificationWebResourceListResponseOut"])
    types["SiteVerificationWebResourceGettokenRequestIn"] = t.struct(
        {
            "site": t.struct(
                {"type": t.string().optional(), "identifier": t.string().optional()}
            ).optional(),
            "verificationMethod": t.string().optional(),
        }
    ).named(renames["SiteVerificationWebResourceGettokenRequestIn"])
    types["SiteVerificationWebResourceGettokenRequestOut"] = t.struct(
        {
            "site": t.struct(
                {"type": t.string().optional(), "identifier": t.string().optional()}
            ).optional(),
            "verificationMethod": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["SiteVerificationWebResourceGettokenRequestOut"])
    types["SiteVerificationWebResourceGettokenResponseIn"] = t.struct(
        {"token": t.string().optional(), "method": t.string().optional()}
    ).named(renames["SiteVerificationWebResourceGettokenResponseIn"])
    types["SiteVerificationWebResourceGettokenResponseOut"] = t.struct(
        {
            "token": t.string().optional(),
            "method": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["SiteVerificationWebResourceGettokenResponseOut"])
    types["SiteVerificationWebResourceResourceIn"] = t.struct(
        {
            "owners": t.array(t.string()).optional(),
            "id": t.string().optional(),
            "site": t.struct(
                {"type": t.string().optional(), "identifier": t.string().optional()}
            ).optional(),
        }
    ).named(renames["SiteVerificationWebResourceResourceIn"])
    types["SiteVerificationWebResourceResourceOut"] = t.struct(
        {
            "owners": t.array(t.string()).optional(),
            "id": t.string().optional(),
            "site": t.struct(
                {"type": t.string().optional(), "identifier": t.string().optional()}
            ).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["SiteVerificationWebResourceResourceOut"])

    functions = {}
    functions["webResourceInsert"] = siteVerification.delete(
        "webResource/{id}",
        t.struct({"id": t.string().optional(), "auth": t.string().optional()}),
        t.struct({"_": t.string().optional()}),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions["webResourceList"] = siteVerification.delete(
        "webResource/{id}",
        t.struct({"id": t.string().optional(), "auth": t.string().optional()}),
        t.struct({"_": t.string().optional()}),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions["webResourcePatch"] = siteVerification.delete(
        "webResource/{id}",
        t.struct({"id": t.string().optional(), "auth": t.string().optional()}),
        t.struct({"_": t.string().optional()}),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions["webResourceGet"] = siteVerification.delete(
        "webResource/{id}",
        t.struct({"id": t.string().optional(), "auth": t.string().optional()}),
        t.struct({"_": t.string().optional()}),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions["webResourceGetToken"] = siteVerification.delete(
        "webResource/{id}",
        t.struct({"id": t.string().optional(), "auth": t.string().optional()}),
        t.struct({"_": t.string().optional()}),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions["webResourceUpdate"] = siteVerification.delete(
        "webResource/{id}",
        t.struct({"id": t.string().optional(), "auth": t.string().optional()}),
        t.struct({"_": t.string().optional()}),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions["webResourceDelete"] = siteVerification.delete(
        "webResource/{id}",
        t.struct({"id": t.string().optional(), "auth": t.string().optional()}),
        t.struct({"_": t.string().optional()}),
        auth_token_field="auth",
        content_type="application/json",
    )

    return Import(
        importer="siteVerification",
        renames=renames,
        types=Box(types),
        functions=Box(functions),
    )
