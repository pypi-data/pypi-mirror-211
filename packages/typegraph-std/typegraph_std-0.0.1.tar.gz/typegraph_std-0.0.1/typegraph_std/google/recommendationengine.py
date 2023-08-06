from typegraph import t
from box import Box
from typegraph.importers.base.importer import Import
from typegraph.runtimes.http import HTTPRuntime


def import_recommendationengine() -> Import:
    recommendationengine = HTTPRuntime("https://recommendationengine.googleapis.com/")

    renames = {
        "ErrorResponse": "_recommendationengine_1_ErrorResponse",
        "GoogleCloudRecommendationengineV1alphaRejoinCatalogMetadataIn": "_recommendationengine_2_GoogleCloudRecommendationengineV1alphaRejoinCatalogMetadataIn",
        "GoogleCloudRecommendationengineV1alphaRejoinCatalogMetadataOut": "_recommendationengine_3_GoogleCloudRecommendationengineV1alphaRejoinCatalogMetadataOut",
        "GoogleCloudRecommendationengineV1beta1FeatureMapIn": "_recommendationengine_4_GoogleCloudRecommendationengineV1beta1FeatureMapIn",
        "GoogleCloudRecommendationengineV1beta1FeatureMapOut": "_recommendationengine_5_GoogleCloudRecommendationengineV1beta1FeatureMapOut",
        "GoogleCloudRecommendationengineV1beta1ProductCatalogItemPriceRangeIn": "_recommendationengine_6_GoogleCloudRecommendationengineV1beta1ProductCatalogItemPriceRangeIn",
        "GoogleCloudRecommendationengineV1beta1ProductCatalogItemPriceRangeOut": "_recommendationengine_7_GoogleCloudRecommendationengineV1beta1ProductCatalogItemPriceRangeOut",
        "GoogleCloudRecommendationengineV1alphaTuningMetadataIn": "_recommendationengine_8_GoogleCloudRecommendationengineV1alphaTuningMetadataIn",
        "GoogleCloudRecommendationengineV1alphaTuningMetadataOut": "_recommendationengine_9_GoogleCloudRecommendationengineV1alphaTuningMetadataOut",
        "GoogleCloudRecommendationengineV1beta1ListCatalogItemsResponseIn": "_recommendationengine_10_GoogleCloudRecommendationengineV1beta1ListCatalogItemsResponseIn",
        "GoogleCloudRecommendationengineV1beta1ListCatalogItemsResponseOut": "_recommendationengine_11_GoogleCloudRecommendationengineV1beta1ListCatalogItemsResponseOut",
        "GoogleCloudRecommendationengineV1beta1FeatureMapStringListIn": "_recommendationengine_12_GoogleCloudRecommendationengineV1beta1FeatureMapStringListIn",
        "GoogleCloudRecommendationengineV1beta1FeatureMapStringListOut": "_recommendationengine_13_GoogleCloudRecommendationengineV1beta1FeatureMapStringListOut",
        "GoogleCloudRecommendationengineV1beta1PurgeUserEventsRequestIn": "_recommendationengine_14_GoogleCloudRecommendationengineV1beta1PurgeUserEventsRequestIn",
        "GoogleCloudRecommendationengineV1beta1PurgeUserEventsRequestOut": "_recommendationengine_15_GoogleCloudRecommendationengineV1beta1PurgeUserEventsRequestOut",
        "GoogleCloudRecommendationengineV1beta1UserEventInlineSourceIn": "_recommendationengine_16_GoogleCloudRecommendationengineV1beta1UserEventInlineSourceIn",
        "GoogleCloudRecommendationengineV1beta1UserEventInlineSourceOut": "_recommendationengine_17_GoogleCloudRecommendationengineV1beta1UserEventInlineSourceOut",
        "GoogleCloudRecommendationengineV1beta1RejoinUserEventsMetadataIn": "_recommendationengine_18_GoogleCloudRecommendationengineV1beta1RejoinUserEventsMetadataIn",
        "GoogleCloudRecommendationengineV1beta1RejoinUserEventsMetadataOut": "_recommendationengine_19_GoogleCloudRecommendationengineV1beta1RejoinUserEventsMetadataOut",
        "GoogleCloudRecommendationengineV1beta1FeatureMapFloatListIn": "_recommendationengine_20_GoogleCloudRecommendationengineV1beta1FeatureMapFloatListIn",
        "GoogleCloudRecommendationengineV1beta1FeatureMapFloatListOut": "_recommendationengine_21_GoogleCloudRecommendationengineV1beta1FeatureMapFloatListOut",
        "GoogleLongrunningListOperationsResponseIn": "_recommendationengine_22_GoogleLongrunningListOperationsResponseIn",
        "GoogleLongrunningListOperationsResponseOut": "_recommendationengine_23_GoogleLongrunningListOperationsResponseOut",
        "GoogleRpcStatusIn": "_recommendationengine_24_GoogleRpcStatusIn",
        "GoogleRpcStatusOut": "_recommendationengine_25_GoogleRpcStatusOut",
        "GoogleCloudRecommendationengineV1beta1ProductDetailIn": "_recommendationengine_26_GoogleCloudRecommendationengineV1beta1ProductDetailIn",
        "GoogleCloudRecommendationengineV1beta1ProductDetailOut": "_recommendationengine_27_GoogleCloudRecommendationengineV1beta1ProductDetailOut",
        "GoogleProtobufEmptyIn": "_recommendationengine_28_GoogleProtobufEmptyIn",
        "GoogleProtobufEmptyOut": "_recommendationengine_29_GoogleProtobufEmptyOut",
        "GoogleCloudRecommendationengineV1beta1ProductCatalogItemExactPriceIn": "_recommendationengine_30_GoogleCloudRecommendationengineV1beta1ProductCatalogItemExactPriceIn",
        "GoogleCloudRecommendationengineV1beta1ProductCatalogItemExactPriceOut": "_recommendationengine_31_GoogleCloudRecommendationengineV1beta1ProductCatalogItemExactPriceOut",
        "GoogleCloudRecommendationengineV1beta1ImportCatalogItemsResponseIn": "_recommendationengine_32_GoogleCloudRecommendationengineV1beta1ImportCatalogItemsResponseIn",
        "GoogleCloudRecommendationengineV1beta1ImportCatalogItemsResponseOut": "_recommendationengine_33_GoogleCloudRecommendationengineV1beta1ImportCatalogItemsResponseOut",
        "GoogleCloudRecommendationengineV1beta1CreatePredictionApiKeyRegistrationRequestIn": "_recommendationengine_34_GoogleCloudRecommendationengineV1beta1CreatePredictionApiKeyRegistrationRequestIn",
        "GoogleCloudRecommendationengineV1beta1CreatePredictionApiKeyRegistrationRequestOut": "_recommendationengine_35_GoogleCloudRecommendationengineV1beta1CreatePredictionApiKeyRegistrationRequestOut",
        "GoogleCloudRecommendationengineV1beta1ImportErrorsConfigIn": "_recommendationengine_36_GoogleCloudRecommendationengineV1beta1ImportErrorsConfigIn",
        "GoogleCloudRecommendationengineV1beta1ImportErrorsConfigOut": "_recommendationengine_37_GoogleCloudRecommendationengineV1beta1ImportErrorsConfigOut",
        "GoogleCloudRecommendationengineV1beta1BigQuerySourceIn": "_recommendationengine_38_GoogleCloudRecommendationengineV1beta1BigQuerySourceIn",
        "GoogleCloudRecommendationengineV1beta1BigQuerySourceOut": "_recommendationengine_39_GoogleCloudRecommendationengineV1beta1BigQuerySourceOut",
        "GoogleCloudRecommendationengineV1beta1ImportUserEventsRequestIn": "_recommendationengine_40_GoogleCloudRecommendationengineV1beta1ImportUserEventsRequestIn",
        "GoogleCloudRecommendationengineV1beta1ImportUserEventsRequestOut": "_recommendationengine_41_GoogleCloudRecommendationengineV1beta1ImportUserEventsRequestOut",
        "GoogleCloudRecommendationengineV1beta1PredictRequestIn": "_recommendationengine_42_GoogleCloudRecommendationengineV1beta1PredictRequestIn",
        "GoogleCloudRecommendationengineV1beta1PredictRequestOut": "_recommendationengine_43_GoogleCloudRecommendationengineV1beta1PredictRequestOut",
        "GoogleApiHttpBodyIn": "_recommendationengine_44_GoogleApiHttpBodyIn",
        "GoogleApiHttpBodyOut": "_recommendationengine_45_GoogleApiHttpBodyOut",
        "GoogleCloudRecommendationengineV1beta1PurgeUserEventsMetadataIn": "_recommendationengine_46_GoogleCloudRecommendationengineV1beta1PurgeUserEventsMetadataIn",
        "GoogleCloudRecommendationengineV1beta1PurgeUserEventsMetadataOut": "_recommendationengine_47_GoogleCloudRecommendationengineV1beta1PurgeUserEventsMetadataOut",
        "GoogleCloudRecommendationengineV1beta1CatalogItemIn": "_recommendationengine_48_GoogleCloudRecommendationengineV1beta1CatalogItemIn",
        "GoogleCloudRecommendationengineV1beta1CatalogItemOut": "_recommendationengine_49_GoogleCloudRecommendationengineV1beta1CatalogItemOut",
        "GoogleCloudRecommendationengineV1alphaRejoinCatalogResponseIn": "_recommendationengine_50_GoogleCloudRecommendationengineV1alphaRejoinCatalogResponseIn",
        "GoogleCloudRecommendationengineV1alphaRejoinCatalogResponseOut": "_recommendationengine_51_GoogleCloudRecommendationengineV1alphaRejoinCatalogResponseOut",
        "GoogleCloudRecommendationengineV1beta1ProductEventDetailIn": "_recommendationengine_52_GoogleCloudRecommendationengineV1beta1ProductEventDetailIn",
        "GoogleCloudRecommendationengineV1beta1ProductEventDetailOut": "_recommendationengine_53_GoogleCloudRecommendationengineV1beta1ProductEventDetailOut",
        "GoogleCloudRecommendationengineV1beta1RejoinUserEventsRequestIn": "_recommendationengine_54_GoogleCloudRecommendationengineV1beta1RejoinUserEventsRequestIn",
        "GoogleCloudRecommendationengineV1beta1RejoinUserEventsRequestOut": "_recommendationengine_55_GoogleCloudRecommendationengineV1beta1RejoinUserEventsRequestOut",
        "GoogleCloudRecommendationengineV1beta1ImageIn": "_recommendationengine_56_GoogleCloudRecommendationengineV1beta1ImageIn",
        "GoogleCloudRecommendationengineV1beta1ImageOut": "_recommendationengine_57_GoogleCloudRecommendationengineV1beta1ImageOut",
        "GoogleCloudRecommendationengineV1beta1CatalogInlineSourceIn": "_recommendationengine_58_GoogleCloudRecommendationengineV1beta1CatalogInlineSourceIn",
        "GoogleCloudRecommendationengineV1beta1CatalogInlineSourceOut": "_recommendationengine_59_GoogleCloudRecommendationengineV1beta1CatalogInlineSourceOut",
        "GoogleCloudRecommendationengineV1beta1ImportCatalogItemsRequestIn": "_recommendationengine_60_GoogleCloudRecommendationengineV1beta1ImportCatalogItemsRequestIn",
        "GoogleCloudRecommendationengineV1beta1ImportCatalogItemsRequestOut": "_recommendationengine_61_GoogleCloudRecommendationengineV1beta1ImportCatalogItemsRequestOut",
        "GoogleCloudRecommendationengineV1beta1UserInfoIn": "_recommendationengine_62_GoogleCloudRecommendationengineV1beta1UserInfoIn",
        "GoogleCloudRecommendationengineV1beta1UserInfoOut": "_recommendationengine_63_GoogleCloudRecommendationengineV1beta1UserInfoOut",
        "GoogleLongrunningOperationIn": "_recommendationengine_64_GoogleLongrunningOperationIn",
        "GoogleLongrunningOperationOut": "_recommendationengine_65_GoogleLongrunningOperationOut",
        "GoogleCloudRecommendationengineV1beta1UserEventIn": "_recommendationengine_66_GoogleCloudRecommendationengineV1beta1UserEventIn",
        "GoogleCloudRecommendationengineV1beta1UserEventOut": "_recommendationengine_67_GoogleCloudRecommendationengineV1beta1UserEventOut",
        "GoogleCloudRecommendationengineV1beta1CatalogItemLevelConfigIn": "_recommendationengine_68_GoogleCloudRecommendationengineV1beta1CatalogItemLevelConfigIn",
        "GoogleCloudRecommendationengineV1beta1CatalogItemLevelConfigOut": "_recommendationengine_69_GoogleCloudRecommendationengineV1beta1CatalogItemLevelConfigOut",
        "GoogleCloudRecommendationengineV1beta1ImportUserEventsResponseIn": "_recommendationengine_70_GoogleCloudRecommendationengineV1beta1ImportUserEventsResponseIn",
        "GoogleCloudRecommendationengineV1beta1ImportUserEventsResponseOut": "_recommendationengine_71_GoogleCloudRecommendationengineV1beta1ImportUserEventsResponseOut",
        "GoogleCloudRecommendationengineV1beta1EventDetailIn": "_recommendationengine_72_GoogleCloudRecommendationengineV1beta1EventDetailIn",
        "GoogleCloudRecommendationengineV1beta1EventDetailOut": "_recommendationengine_73_GoogleCloudRecommendationengineV1beta1EventDetailOut",
        "GoogleCloudRecommendationengineV1beta1CatalogIn": "_recommendationengine_74_GoogleCloudRecommendationengineV1beta1CatalogIn",
        "GoogleCloudRecommendationengineV1beta1CatalogOut": "_recommendationengine_75_GoogleCloudRecommendationengineV1beta1CatalogOut",
        "GoogleCloudRecommendationengineV1beta1PredictResponseIn": "_recommendationengine_76_GoogleCloudRecommendationengineV1beta1PredictResponseIn",
        "GoogleCloudRecommendationengineV1beta1PredictResponseOut": "_recommendationengine_77_GoogleCloudRecommendationengineV1beta1PredictResponseOut",
        "GoogleCloudRecommendationengineV1beta1UserEventImportSummaryIn": "_recommendationengine_78_GoogleCloudRecommendationengineV1beta1UserEventImportSummaryIn",
        "GoogleCloudRecommendationengineV1beta1UserEventImportSummaryOut": "_recommendationengine_79_GoogleCloudRecommendationengineV1beta1UserEventImportSummaryOut",
        "GoogleCloudRecommendationengineV1beta1RejoinUserEventsResponseIn": "_recommendationengine_80_GoogleCloudRecommendationengineV1beta1RejoinUserEventsResponseIn",
        "GoogleCloudRecommendationengineV1beta1RejoinUserEventsResponseOut": "_recommendationengine_81_GoogleCloudRecommendationengineV1beta1RejoinUserEventsResponseOut",
        "GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyIn": "_recommendationengine_82_GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyIn",
        "GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyOut": "_recommendationengine_83_GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyOut",
        "GoogleCloudRecommendationengineV1beta1ListCatalogsResponseIn": "_recommendationengine_84_GoogleCloudRecommendationengineV1beta1ListCatalogsResponseIn",
        "GoogleCloudRecommendationengineV1beta1ListCatalogsResponseOut": "_recommendationengine_85_GoogleCloudRecommendationengineV1beta1ListCatalogsResponseOut",
        "GoogleCloudRecommendationengineV1beta1PurgeUserEventsResponseIn": "_recommendationengine_86_GoogleCloudRecommendationengineV1beta1PurgeUserEventsResponseIn",
        "GoogleCloudRecommendationengineV1beta1PurgeUserEventsResponseOut": "_recommendationengine_87_GoogleCloudRecommendationengineV1beta1PurgeUserEventsResponseOut",
        "GoogleCloudRecommendationengineV1beta1PredictResponsePredictionResultIn": "_recommendationengine_88_GoogleCloudRecommendationengineV1beta1PredictResponsePredictionResultIn",
        "GoogleCloudRecommendationengineV1beta1PredictResponsePredictionResultOut": "_recommendationengine_89_GoogleCloudRecommendationengineV1beta1PredictResponsePredictionResultOut",
        "GoogleCloudRecommendationengineV1beta1PurchaseTransactionIn": "_recommendationengine_90_GoogleCloudRecommendationengineV1beta1PurchaseTransactionIn",
        "GoogleCloudRecommendationengineV1beta1PurchaseTransactionOut": "_recommendationengine_91_GoogleCloudRecommendationengineV1beta1PurchaseTransactionOut",
        "GoogleCloudRecommendationengineV1beta1InputConfigIn": "_recommendationengine_92_GoogleCloudRecommendationengineV1beta1InputConfigIn",
        "GoogleCloudRecommendationengineV1beta1InputConfigOut": "_recommendationengine_93_GoogleCloudRecommendationengineV1beta1InputConfigOut",
        "GoogleCloudRecommendationengineV1beta1ImportMetadataIn": "_recommendationengine_94_GoogleCloudRecommendationengineV1beta1ImportMetadataIn",
        "GoogleCloudRecommendationengineV1beta1ImportMetadataOut": "_recommendationengine_95_GoogleCloudRecommendationengineV1beta1ImportMetadataOut",
        "GoogleCloudRecommendationengineV1alphaTuningResponseIn": "_recommendationengine_96_GoogleCloudRecommendationengineV1alphaTuningResponseIn",
        "GoogleCloudRecommendationengineV1alphaTuningResponseOut": "_recommendationengine_97_GoogleCloudRecommendationengineV1alphaTuningResponseOut",
        "GoogleCloudRecommendationengineV1beta1ListPredictionApiKeyRegistrationsResponseIn": "_recommendationengine_98_GoogleCloudRecommendationengineV1beta1ListPredictionApiKeyRegistrationsResponseIn",
        "GoogleCloudRecommendationengineV1beta1ListPredictionApiKeyRegistrationsResponseOut": "_recommendationengine_99_GoogleCloudRecommendationengineV1beta1ListPredictionApiKeyRegistrationsResponseOut",
        "GoogleCloudRecommendationengineV1beta1GcsSourceIn": "_recommendationengine_100_GoogleCloudRecommendationengineV1beta1GcsSourceIn",
        "GoogleCloudRecommendationengineV1beta1GcsSourceOut": "_recommendationengine_101_GoogleCloudRecommendationengineV1beta1GcsSourceOut",
        "GoogleCloudRecommendationengineV1beta1ListUserEventsResponseIn": "_recommendationengine_102_GoogleCloudRecommendationengineV1beta1ListUserEventsResponseIn",
        "GoogleCloudRecommendationengineV1beta1ListUserEventsResponseOut": "_recommendationengine_103_GoogleCloudRecommendationengineV1beta1ListUserEventsResponseOut",
        "GoogleCloudRecommendationengineV1beta1ProductCatalogItemIn": "_recommendationengine_104_GoogleCloudRecommendationengineV1beta1ProductCatalogItemIn",
        "GoogleCloudRecommendationengineV1beta1ProductCatalogItemOut": "_recommendationengine_105_GoogleCloudRecommendationengineV1beta1ProductCatalogItemOut",
        "GoogleCloudRecommendationengineV1beta1PredictionApiKeyRegistrationIn": "_recommendationengine_106_GoogleCloudRecommendationengineV1beta1PredictionApiKeyRegistrationIn",
        "GoogleCloudRecommendationengineV1beta1PredictionApiKeyRegistrationOut": "_recommendationengine_107_GoogleCloudRecommendationengineV1beta1PredictionApiKeyRegistrationOut",
    }

    types = {}
    types["ErrorResponse"] = t.struct(
        {"code": t.integer(), "message": t.string(), "status": t.string()}
    ).named(renames["ErrorResponse"])
    types["GoogleCloudRecommendationengineV1alphaRejoinCatalogMetadataIn"] = t.struct(
        {"_": t.string().optional()}
    ).named(renames["GoogleCloudRecommendationengineV1alphaRejoinCatalogMetadataIn"])
    types["GoogleCloudRecommendationengineV1alphaRejoinCatalogMetadataOut"] = t.struct(
        {"error": t.proxy(renames["ErrorResponse"]).optional()}
    ).named(renames["GoogleCloudRecommendationengineV1alphaRejoinCatalogMetadataOut"])
    types["GoogleCloudRecommendationengineV1beta1FeatureMapIn"] = t.struct(
        {
            "numericalFeatures": t.struct({"_": t.string().optional()}).optional(),
            "categoricalFeatures": t.struct({"_": t.string().optional()}).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1FeatureMapIn"])
    types["GoogleCloudRecommendationengineV1beta1FeatureMapOut"] = t.struct(
        {
            "numericalFeatures": t.struct({"_": t.string().optional()}).optional(),
            "categoricalFeatures": t.struct({"_": t.string().optional()}).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1FeatureMapOut"])
    types[
        "GoogleCloudRecommendationengineV1beta1ProductCatalogItemPriceRangeIn"
    ] = t.struct({"max": t.number(), "min": t.number()}).named(
        renames["GoogleCloudRecommendationengineV1beta1ProductCatalogItemPriceRangeIn"]
    )
    types[
        "GoogleCloudRecommendationengineV1beta1ProductCatalogItemPriceRangeOut"
    ] = t.struct(
        {
            "max": t.number(),
            "min": t.number(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1ProductCatalogItemPriceRangeOut"]
    )
    types["GoogleCloudRecommendationengineV1alphaTuningMetadataIn"] = t.struct(
        {"recommendationModel": t.string().optional()}
    ).named(renames["GoogleCloudRecommendationengineV1alphaTuningMetadataIn"])
    types["GoogleCloudRecommendationengineV1alphaTuningMetadataOut"] = t.struct(
        {
            "recommendationModel": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1alphaTuningMetadataOut"])
    types[
        "GoogleCloudRecommendationengineV1beta1ListCatalogItemsResponseIn"
    ] = t.struct(
        {
            "catalogItems": t.array(
                t.proxy(renames["GoogleCloudRecommendationengineV1beta1CatalogItemIn"])
            ).optional(),
            "nextPageToken": t.string().optional(),
        }
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1ListCatalogItemsResponseIn"]
    )
    types[
        "GoogleCloudRecommendationengineV1beta1ListCatalogItemsResponseOut"
    ] = t.struct(
        {
            "catalogItems": t.array(
                t.proxy(renames["GoogleCloudRecommendationengineV1beta1CatalogItemOut"])
            ).optional(),
            "nextPageToken": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1ListCatalogItemsResponseOut"]
    )
    types["GoogleCloudRecommendationengineV1beta1FeatureMapStringListIn"] = t.struct(
        {"value": t.array(t.string()).optional()}
    ).named(renames["GoogleCloudRecommendationengineV1beta1FeatureMapStringListIn"])
    types["GoogleCloudRecommendationengineV1beta1FeatureMapStringListOut"] = t.struct(
        {
            "value": t.array(t.string()).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1FeatureMapStringListOut"])
    types["GoogleCloudRecommendationengineV1beta1PurgeUserEventsRequestIn"] = t.struct(
        {"filter": t.string(), "force": t.boolean().optional()}
    ).named(renames["GoogleCloudRecommendationengineV1beta1PurgeUserEventsRequestIn"])
    types["GoogleCloudRecommendationengineV1beta1PurgeUserEventsRequestOut"] = t.struct(
        {
            "filter": t.string(),
            "force": t.boolean().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1PurgeUserEventsRequestOut"])
    types["GoogleCloudRecommendationengineV1beta1UserEventInlineSourceIn"] = t.struct(
        {
            "userEvents": t.array(
                t.proxy(renames["GoogleCloudRecommendationengineV1beta1UserEventIn"])
            ).optional()
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1UserEventInlineSourceIn"])
    types["GoogleCloudRecommendationengineV1beta1UserEventInlineSourceOut"] = t.struct(
        {
            "userEvents": t.array(
                t.proxy(renames["GoogleCloudRecommendationengineV1beta1UserEventOut"])
            ).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1UserEventInlineSourceOut"])
    types[
        "GoogleCloudRecommendationengineV1beta1RejoinUserEventsMetadataIn"
    ] = t.struct({"_": t.string().optional()}).named(
        renames["GoogleCloudRecommendationengineV1beta1RejoinUserEventsMetadataIn"]
    )
    types[
        "GoogleCloudRecommendationengineV1beta1RejoinUserEventsMetadataOut"
    ] = t.struct({"error": t.proxy(renames["ErrorResponse"]).optional()}).named(
        renames["GoogleCloudRecommendationengineV1beta1RejoinUserEventsMetadataOut"]
    )
    types["GoogleCloudRecommendationengineV1beta1FeatureMapFloatListIn"] = t.struct(
        {"value": t.array(t.number()).optional()}
    ).named(renames["GoogleCloudRecommendationengineV1beta1FeatureMapFloatListIn"])
    types["GoogleCloudRecommendationengineV1beta1FeatureMapFloatListOut"] = t.struct(
        {
            "value": t.array(t.number()).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1FeatureMapFloatListOut"])
    types["GoogleLongrunningListOperationsResponseIn"] = t.struct(
        {
            "nextPageToken": t.string().optional(),
            "operations": t.array(
                t.proxy(renames["GoogleLongrunningOperationIn"])
            ).optional(),
        }
    ).named(renames["GoogleLongrunningListOperationsResponseIn"])
    types["GoogleLongrunningListOperationsResponseOut"] = t.struct(
        {
            "nextPageToken": t.string().optional(),
            "operations": t.array(
                t.proxy(renames["GoogleLongrunningOperationOut"])
            ).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleLongrunningListOperationsResponseOut"])
    types["GoogleRpcStatusIn"] = t.struct(
        {
            "details": t.array(t.struct({"_": t.string().optional()})).optional(),
            "message": t.string().optional(),
            "code": t.integer().optional(),
        }
    ).named(renames["GoogleRpcStatusIn"])
    types["GoogleRpcStatusOut"] = t.struct(
        {
            "details": t.array(t.struct({"_": t.string().optional()})).optional(),
            "message": t.string().optional(),
            "code": t.integer().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleRpcStatusOut"])
    types["GoogleCloudRecommendationengineV1beta1ProductDetailIn"] = t.struct(
        {
            "availableQuantity": t.integer().optional(),
            "quantity": t.integer().optional(),
            "itemAttributes": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1FeatureMapIn"]
            ).optional(),
            "stockState": t.string().optional(),
            "displayPrice": t.number().optional(),
            "currencyCode": t.string().optional(),
            "originalPrice": t.number().optional(),
            "id": t.string(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1ProductDetailIn"])
    types["GoogleCloudRecommendationengineV1beta1ProductDetailOut"] = t.struct(
        {
            "availableQuantity": t.integer().optional(),
            "quantity": t.integer().optional(),
            "itemAttributes": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1FeatureMapOut"]
            ).optional(),
            "stockState": t.string().optional(),
            "displayPrice": t.number().optional(),
            "currencyCode": t.string().optional(),
            "originalPrice": t.number().optional(),
            "id": t.string(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1ProductDetailOut"])
    types["GoogleProtobufEmptyIn"] = t.struct({"_": t.string().optional()}).named(
        renames["GoogleProtobufEmptyIn"]
    )
    types["GoogleProtobufEmptyOut"] = t.struct(
        {"error": t.proxy(renames["ErrorResponse"]).optional()}
    ).named(renames["GoogleProtobufEmptyOut"])
    types[
        "GoogleCloudRecommendationengineV1beta1ProductCatalogItemExactPriceIn"
    ] = t.struct(
        {"originalPrice": t.number().optional(), "displayPrice": t.number().optional()}
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1ProductCatalogItemExactPriceIn"]
    )
    types[
        "GoogleCloudRecommendationengineV1beta1ProductCatalogItemExactPriceOut"
    ] = t.struct(
        {
            "originalPrice": t.number().optional(),
            "displayPrice": t.number().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1ProductCatalogItemExactPriceOut"]
    )
    types[
        "GoogleCloudRecommendationengineV1beta1ImportCatalogItemsResponseIn"
    ] = t.struct(
        {
            "errorSamples": t.array(t.proxy(renames["GoogleRpcStatusIn"])).optional(),
            "errorsConfig": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1ImportErrorsConfigIn"]
            ).optional(),
        }
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1ImportCatalogItemsResponseIn"]
    )
    types[
        "GoogleCloudRecommendationengineV1beta1ImportCatalogItemsResponseOut"
    ] = t.struct(
        {
            "errorSamples": t.array(t.proxy(renames["GoogleRpcStatusOut"])).optional(),
            "errorsConfig": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1ImportErrorsConfigOut"]
            ).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1ImportCatalogItemsResponseOut"]
    )
    types[
        "GoogleCloudRecommendationengineV1beta1CreatePredictionApiKeyRegistrationRequestIn"
    ] = t.struct(
        {
            "predictionApiKeyRegistration": t.proxy(
                renames[
                    "GoogleCloudRecommendationengineV1beta1PredictionApiKeyRegistrationIn"
                ]
            )
        }
    ).named(
        renames[
            "GoogleCloudRecommendationengineV1beta1CreatePredictionApiKeyRegistrationRequestIn"
        ]
    )
    types[
        "GoogleCloudRecommendationengineV1beta1CreatePredictionApiKeyRegistrationRequestOut"
    ] = t.struct(
        {
            "predictionApiKeyRegistration": t.proxy(
                renames[
                    "GoogleCloudRecommendationengineV1beta1PredictionApiKeyRegistrationOut"
                ]
            ),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(
        renames[
            "GoogleCloudRecommendationengineV1beta1CreatePredictionApiKeyRegistrationRequestOut"
        ]
    )
    types["GoogleCloudRecommendationengineV1beta1ImportErrorsConfigIn"] = t.struct(
        {"gcsPrefix": t.string().optional()}
    ).named(renames["GoogleCloudRecommendationengineV1beta1ImportErrorsConfigIn"])
    types["GoogleCloudRecommendationengineV1beta1ImportErrorsConfigOut"] = t.struct(
        {
            "gcsPrefix": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1ImportErrorsConfigOut"])
    types["GoogleCloudRecommendationengineV1beta1BigQuerySourceIn"] = t.struct(
        {
            "gcsStagingDir": t.string().optional(),
            "tableId": t.string(),
            "dataSchema": t.string().optional(),
            "projectId": t.string().optional(),
            "datasetId": t.string(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1BigQuerySourceIn"])
    types["GoogleCloudRecommendationengineV1beta1BigQuerySourceOut"] = t.struct(
        {
            "gcsStagingDir": t.string().optional(),
            "tableId": t.string(),
            "dataSchema": t.string().optional(),
            "projectId": t.string().optional(),
            "datasetId": t.string(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1BigQuerySourceOut"])
    types["GoogleCloudRecommendationengineV1beta1ImportUserEventsRequestIn"] = t.struct(
        {
            "inputConfig": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1InputConfigIn"]
            ),
            "requestId": t.string().optional(),
            "errorsConfig": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1ImportErrorsConfigIn"]
            ).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1ImportUserEventsRequestIn"])
    types[
        "GoogleCloudRecommendationengineV1beta1ImportUserEventsRequestOut"
    ] = t.struct(
        {
            "inputConfig": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1InputConfigOut"]
            ),
            "requestId": t.string().optional(),
            "errorsConfig": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1ImportErrorsConfigOut"]
            ).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1ImportUserEventsRequestOut"]
    )
    types["GoogleCloudRecommendationengineV1beta1PredictRequestIn"] = t.struct(
        {
            "pageToken": t.string().optional(),
            "pageSize": t.integer().optional(),
            "userEvent": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1UserEventIn"]
            ),
            "dryRun": t.boolean().optional(),
            "params": t.struct({"_": t.string().optional()}).optional(),
            "labels": t.struct({"_": t.string().optional()}).optional(),
            "filter": t.string().optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1PredictRequestIn"])
    types["GoogleCloudRecommendationengineV1beta1PredictRequestOut"] = t.struct(
        {
            "pageToken": t.string().optional(),
            "pageSize": t.integer().optional(),
            "userEvent": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1UserEventOut"]
            ),
            "dryRun": t.boolean().optional(),
            "params": t.struct({"_": t.string().optional()}).optional(),
            "labels": t.struct({"_": t.string().optional()}).optional(),
            "filter": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1PredictRequestOut"])
    types["GoogleApiHttpBodyIn"] = t.struct(
        {
            "contentType": t.string().optional(),
            "data": t.string().optional(),
            "extensions": t.array(t.struct({"_": t.string().optional()})).optional(),
        }
    ).named(renames["GoogleApiHttpBodyIn"])
    types["GoogleApiHttpBodyOut"] = t.struct(
        {
            "contentType": t.string().optional(),
            "data": t.string().optional(),
            "extensions": t.array(t.struct({"_": t.string().optional()})).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleApiHttpBodyOut"])
    types["GoogleCloudRecommendationengineV1beta1PurgeUserEventsMetadataIn"] = t.struct(
        {"createTime": t.string().optional(), "operationName": t.string().optional()}
    ).named(renames["GoogleCloudRecommendationengineV1beta1PurgeUserEventsMetadataIn"])
    types[
        "GoogleCloudRecommendationengineV1beta1PurgeUserEventsMetadataOut"
    ] = t.struct(
        {
            "createTime": t.string().optional(),
            "operationName": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1PurgeUserEventsMetadataOut"]
    )
    types["GoogleCloudRecommendationengineV1beta1CatalogItemIn"] = t.struct(
        {
            "categoryHierarchies": t.array(
                t.proxy(
                    renames[
                        "GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyIn"
                    ]
                )
            ),
            "id": t.string(),
            "itemAttributes": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1FeatureMapIn"]
            ).optional(),
            "languageCode": t.string().optional(),
            "description": t.string().optional(),
            "productMetadata": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1ProductCatalogItemIn"]
            ).optional(),
            "tags": t.array(t.string()).optional(),
            "itemGroupId": t.string().optional(),
            "title": t.string(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1CatalogItemIn"])
    types["GoogleCloudRecommendationengineV1beta1CatalogItemOut"] = t.struct(
        {
            "categoryHierarchies": t.array(
                t.proxy(
                    renames[
                        "GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyOut"
                    ]
                )
            ),
            "id": t.string(),
            "itemAttributes": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1FeatureMapOut"]
            ).optional(),
            "languageCode": t.string().optional(),
            "description": t.string().optional(),
            "productMetadata": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1ProductCatalogItemOut"]
            ).optional(),
            "tags": t.array(t.string()).optional(),
            "itemGroupId": t.string().optional(),
            "title": t.string(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1CatalogItemOut"])
    types["GoogleCloudRecommendationengineV1alphaRejoinCatalogResponseIn"] = t.struct(
        {"rejoinedUserEventsCount": t.string().optional()}
    ).named(renames["GoogleCloudRecommendationengineV1alphaRejoinCatalogResponseIn"])
    types["GoogleCloudRecommendationengineV1alphaRejoinCatalogResponseOut"] = t.struct(
        {
            "rejoinedUserEventsCount": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1alphaRejoinCatalogResponseOut"])
    types["GoogleCloudRecommendationengineV1beta1ProductEventDetailIn"] = t.struct(
        {
            "purchaseTransaction": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1PurchaseTransactionIn"]
            ).optional(),
            "pageCategories": t.array(
                t.proxy(
                    renames[
                        "GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyIn"
                    ]
                )
            ),
            "productDetails": t.array(
                t.proxy(
                    renames["GoogleCloudRecommendationengineV1beta1ProductDetailIn"]
                )
            ).optional(),
            "listId": t.string(),
            "cartId": t.string().optional(),
            "searchQuery": t.string().optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1ProductEventDetailIn"])
    types["GoogleCloudRecommendationengineV1beta1ProductEventDetailOut"] = t.struct(
        {
            "purchaseTransaction": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1PurchaseTransactionOut"]
            ).optional(),
            "pageCategories": t.array(
                t.proxy(
                    renames[
                        "GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyOut"
                    ]
                )
            ),
            "productDetails": t.array(
                t.proxy(
                    renames["GoogleCloudRecommendationengineV1beta1ProductDetailOut"]
                )
            ).optional(),
            "listId": t.string(),
            "cartId": t.string().optional(),
            "searchQuery": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1ProductEventDetailOut"])
    types["GoogleCloudRecommendationengineV1beta1RejoinUserEventsRequestIn"] = t.struct(
        {"userEventRejoinScope": t.string()}
    ).named(renames["GoogleCloudRecommendationengineV1beta1RejoinUserEventsRequestIn"])
    types[
        "GoogleCloudRecommendationengineV1beta1RejoinUserEventsRequestOut"
    ] = t.struct(
        {
            "userEventRejoinScope": t.string(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1RejoinUserEventsRequestOut"]
    )
    types["GoogleCloudRecommendationengineV1beta1ImageIn"] = t.struct(
        {
            "height": t.integer().optional(),
            "width": t.integer().optional(),
            "uri": t.string(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1ImageIn"])
    types["GoogleCloudRecommendationengineV1beta1ImageOut"] = t.struct(
        {
            "height": t.integer().optional(),
            "width": t.integer().optional(),
            "uri": t.string(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1ImageOut"])
    types["GoogleCloudRecommendationengineV1beta1CatalogInlineSourceIn"] = t.struct(
        {
            "catalogItems": t.array(
                t.proxy(renames["GoogleCloudRecommendationengineV1beta1CatalogItemIn"])
            ).optional()
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1CatalogInlineSourceIn"])
    types["GoogleCloudRecommendationengineV1beta1CatalogInlineSourceOut"] = t.struct(
        {
            "catalogItems": t.array(
                t.proxy(renames["GoogleCloudRecommendationengineV1beta1CatalogItemOut"])
            ).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1CatalogInlineSourceOut"])
    types[
        "GoogleCloudRecommendationengineV1beta1ImportCatalogItemsRequestIn"
    ] = t.struct(
        {
            "errorsConfig": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1ImportErrorsConfigIn"]
            ).optional(),
            "updateMask": t.string().optional(),
            "requestId": t.string().optional(),
            "inputConfig": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1InputConfigIn"]
            ),
        }
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1ImportCatalogItemsRequestIn"]
    )
    types[
        "GoogleCloudRecommendationengineV1beta1ImportCatalogItemsRequestOut"
    ] = t.struct(
        {
            "errorsConfig": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1ImportErrorsConfigOut"]
            ).optional(),
            "updateMask": t.string().optional(),
            "requestId": t.string().optional(),
            "inputConfig": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1InputConfigOut"]
            ),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1ImportCatalogItemsRequestOut"]
    )
    types["GoogleCloudRecommendationengineV1beta1UserInfoIn"] = t.struct(
        {
            "ipAddress": t.string().optional(),
            "visitorId": t.string(),
            "userAgent": t.string().optional(),
            "directUserRequest": t.boolean().optional(),
            "userId": t.string().optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1UserInfoIn"])
    types["GoogleCloudRecommendationengineV1beta1UserInfoOut"] = t.struct(
        {
            "ipAddress": t.string().optional(),
            "visitorId": t.string(),
            "userAgent": t.string().optional(),
            "directUserRequest": t.boolean().optional(),
            "userId": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1UserInfoOut"])
    types["GoogleLongrunningOperationIn"] = t.struct(
        {
            "error": t.proxy(renames["GoogleRpcStatusIn"]).optional(),
            "metadata": t.struct({"_": t.string().optional()}).optional(),
            "name": t.string().optional(),
            "done": t.boolean().optional(),
            "response": t.struct({"_": t.string().optional()}).optional(),
        }
    ).named(renames["GoogleLongrunningOperationIn"])
    types["GoogleLongrunningOperationOut"] = t.struct(
        {
            "error": t.proxy(renames["ErrorResponse"]).optional(),
            "metadata": t.struct({"_": t.string().optional()}).optional(),
            "name": t.string().optional(),
            "done": t.boolean().optional(),
            "response": t.struct({"_": t.string().optional()}).optional(),
        }
    ).named(renames["GoogleLongrunningOperationOut"])
    types["GoogleCloudRecommendationengineV1beta1UserEventIn"] = t.struct(
        {
            "eventType": t.string(),
            "eventDetail": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1EventDetailIn"]
            ).optional(),
            "productEventDetail": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1ProductEventDetailIn"]
            ).optional(),
            "userInfo": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1UserInfoIn"]
            ),
            "eventSource": t.string().optional(),
            "eventTime": t.string().optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1UserEventIn"])
    types["GoogleCloudRecommendationengineV1beta1UserEventOut"] = t.struct(
        {
            "eventType": t.string(),
            "eventDetail": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1EventDetailOut"]
            ).optional(),
            "productEventDetail": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1ProductEventDetailOut"]
            ).optional(),
            "userInfo": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1UserInfoOut"]
            ),
            "eventSource": t.string().optional(),
            "eventTime": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1UserEventOut"])
    types["GoogleCloudRecommendationengineV1beta1CatalogItemLevelConfigIn"] = t.struct(
        {
            "eventItemLevel": t.string().optional(),
            "predictItemLevel": t.string().optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1CatalogItemLevelConfigIn"])
    types["GoogleCloudRecommendationengineV1beta1CatalogItemLevelConfigOut"] = t.struct(
        {
            "eventItemLevel": t.string().optional(),
            "predictItemLevel": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1CatalogItemLevelConfigOut"])
    types[
        "GoogleCloudRecommendationengineV1beta1ImportUserEventsResponseIn"
    ] = t.struct(
        {
            "errorSamples": t.array(t.proxy(renames["GoogleRpcStatusIn"])).optional(),
            "importSummary": t.proxy(
                renames[
                    "GoogleCloudRecommendationengineV1beta1UserEventImportSummaryIn"
                ]
            ).optional(),
            "errorsConfig": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1ImportErrorsConfigIn"]
            ).optional(),
        }
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1ImportUserEventsResponseIn"]
    )
    types[
        "GoogleCloudRecommendationengineV1beta1ImportUserEventsResponseOut"
    ] = t.struct(
        {
            "errorSamples": t.array(t.proxy(renames["GoogleRpcStatusOut"])).optional(),
            "importSummary": t.proxy(
                renames[
                    "GoogleCloudRecommendationengineV1beta1UserEventImportSummaryOut"
                ]
            ).optional(),
            "errorsConfig": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1ImportErrorsConfigOut"]
            ).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1ImportUserEventsResponseOut"]
    )
    types["GoogleCloudRecommendationengineV1beta1EventDetailIn"] = t.struct(
        {
            "recommendationToken": t.string().optional(),
            "referrerUri": t.string().optional(),
            "uri": t.string().optional(),
            "eventAttributes": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1FeatureMapIn"]
            ).optional(),
            "experimentIds": t.array(t.string()).optional(),
            "pageViewId": t.string().optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1EventDetailIn"])
    types["GoogleCloudRecommendationengineV1beta1EventDetailOut"] = t.struct(
        {
            "recommendationToken": t.string().optional(),
            "referrerUri": t.string().optional(),
            "uri": t.string().optional(),
            "eventAttributes": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1FeatureMapOut"]
            ).optional(),
            "experimentIds": t.array(t.string()).optional(),
            "pageViewId": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1EventDetailOut"])
    types["GoogleCloudRecommendationengineV1beta1CatalogIn"] = t.struct(
        {
            "catalogItemLevelConfig": t.proxy(
                renames[
                    "GoogleCloudRecommendationengineV1beta1CatalogItemLevelConfigIn"
                ]
            ),
            "defaultEventStoreId": t.string(),
            "name": t.string().optional(),
            "displayName": t.string(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1CatalogIn"])
    types["GoogleCloudRecommendationengineV1beta1CatalogOut"] = t.struct(
        {
            "catalogItemLevelConfig": t.proxy(
                renames[
                    "GoogleCloudRecommendationengineV1beta1CatalogItemLevelConfigOut"
                ]
            ),
            "defaultEventStoreId": t.string(),
            "name": t.string().optional(),
            "displayName": t.string(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1CatalogOut"])
    types["GoogleCloudRecommendationengineV1beta1PredictResponseIn"] = t.struct(
        {
            "dryRun": t.boolean().optional(),
            "nextPageToken": t.string().optional(),
            "results": t.array(
                t.proxy(
                    renames[
                        "GoogleCloudRecommendationengineV1beta1PredictResponsePredictionResultIn"
                    ]
                )
            ).optional(),
            "recommendationToken": t.string().optional(),
            "metadata": t.struct({"_": t.string().optional()}).optional(),
            "itemsMissingInCatalog": t.array(t.string()).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1PredictResponseIn"])
    types["GoogleCloudRecommendationengineV1beta1PredictResponseOut"] = t.struct(
        {
            "dryRun": t.boolean().optional(),
            "nextPageToken": t.string().optional(),
            "results": t.array(
                t.proxy(
                    renames[
                        "GoogleCloudRecommendationengineV1beta1PredictResponsePredictionResultOut"
                    ]
                )
            ).optional(),
            "recommendationToken": t.string().optional(),
            "metadata": t.struct({"_": t.string().optional()}).optional(),
            "itemsMissingInCatalog": t.array(t.string()).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1PredictResponseOut"])
    types["GoogleCloudRecommendationengineV1beta1UserEventImportSummaryIn"] = t.struct(
        {
            "joinedEventsCount": t.string().optional(),
            "unjoinedEventsCount": t.string().optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1UserEventImportSummaryIn"])
    types["GoogleCloudRecommendationengineV1beta1UserEventImportSummaryOut"] = t.struct(
        {
            "joinedEventsCount": t.string().optional(),
            "unjoinedEventsCount": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1UserEventImportSummaryOut"])
    types[
        "GoogleCloudRecommendationengineV1beta1RejoinUserEventsResponseIn"
    ] = t.struct({"rejoinedUserEventsCount": t.string().optional()}).named(
        renames["GoogleCloudRecommendationengineV1beta1RejoinUserEventsResponseIn"]
    )
    types[
        "GoogleCloudRecommendationengineV1beta1RejoinUserEventsResponseOut"
    ] = t.struct(
        {
            "rejoinedUserEventsCount": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1RejoinUserEventsResponseOut"]
    )
    types[
        "GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyIn"
    ] = t.struct({"categories": t.array(t.string())}).named(
        renames["GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyIn"]
    )
    types[
        "GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyOut"
    ] = t.struct(
        {
            "categories": t.array(t.string()),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyOut"]
    )
    types["GoogleCloudRecommendationengineV1beta1ListCatalogsResponseIn"] = t.struct(
        {"nextPageToken": t.string().optional()}
    ).named(renames["GoogleCloudRecommendationengineV1beta1ListCatalogsResponseIn"])
    types["GoogleCloudRecommendationengineV1beta1ListCatalogsResponseOut"] = t.struct(
        {
            "nextPageToken": t.string().optional(),
            "catalogs": t.array(
                t.proxy(renames["GoogleCloudRecommendationengineV1beta1CatalogOut"])
            ).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1ListCatalogsResponseOut"])
    types["GoogleCloudRecommendationengineV1beta1PurgeUserEventsResponseIn"] = t.struct(
        {
            "purgedEventsCount": t.string().optional(),
            "userEventsSample": t.array(
                t.proxy(renames["GoogleCloudRecommendationengineV1beta1UserEventIn"])
            ).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1PurgeUserEventsResponseIn"])
    types[
        "GoogleCloudRecommendationengineV1beta1PurgeUserEventsResponseOut"
    ] = t.struct(
        {
            "purgedEventsCount": t.string().optional(),
            "userEventsSample": t.array(
                t.proxy(renames["GoogleCloudRecommendationengineV1beta1UserEventOut"])
            ).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1PurgeUserEventsResponseOut"]
    )
    types[
        "GoogleCloudRecommendationengineV1beta1PredictResponsePredictionResultIn"
    ] = t.struct(
        {
            "itemMetadata": t.struct({"_": t.string().optional()}).optional(),
            "id": t.string().optional(),
        }
    ).named(
        renames[
            "GoogleCloudRecommendationengineV1beta1PredictResponsePredictionResultIn"
        ]
    )
    types[
        "GoogleCloudRecommendationengineV1beta1PredictResponsePredictionResultOut"
    ] = t.struct(
        {
            "itemMetadata": t.struct({"_": t.string().optional()}).optional(),
            "id": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(
        renames[
            "GoogleCloudRecommendationengineV1beta1PredictResponsePredictionResultOut"
        ]
    )
    types["GoogleCloudRecommendationengineV1beta1PurchaseTransactionIn"] = t.struct(
        {
            "id": t.string().optional(),
            "costs": t.struct({"_": t.string().optional()}).optional(),
            "revenue": t.number(),
            "currencyCode": t.string(),
            "taxes": t.struct({"_": t.string().optional()}).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1PurchaseTransactionIn"])
    types["GoogleCloudRecommendationengineV1beta1PurchaseTransactionOut"] = t.struct(
        {
            "id": t.string().optional(),
            "costs": t.struct({"_": t.string().optional()}).optional(),
            "revenue": t.number(),
            "currencyCode": t.string(),
            "taxes": t.struct({"_": t.string().optional()}).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1PurchaseTransactionOut"])
    types["GoogleCloudRecommendationengineV1beta1InputConfigIn"] = t.struct(
        {
            "bigQuerySource": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1BigQuerySourceIn"]
            ).optional(),
            "userEventInlineSource": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1UserEventInlineSourceIn"]
            ).optional(),
            "gcsSource": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1GcsSourceIn"]
            ).optional(),
            "catalogInlineSource": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1CatalogInlineSourceIn"]
            ).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1InputConfigIn"])
    types["GoogleCloudRecommendationengineV1beta1InputConfigOut"] = t.struct(
        {
            "bigQuerySource": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1BigQuerySourceOut"]
            ).optional(),
            "userEventInlineSource": t.proxy(
                renames[
                    "GoogleCloudRecommendationengineV1beta1UserEventInlineSourceOut"
                ]
            ).optional(),
            "gcsSource": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1GcsSourceOut"]
            ).optional(),
            "catalogInlineSource": t.proxy(
                renames["GoogleCloudRecommendationengineV1beta1CatalogInlineSourceOut"]
            ).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1InputConfigOut"])
    types["GoogleCloudRecommendationengineV1beta1ImportMetadataIn"] = t.struct(
        {
            "operationName": t.string().optional(),
            "failureCount": t.string().optional(),
            "successCount": t.string().optional(),
            "requestId": t.string().optional(),
            "updateTime": t.string().optional(),
            "createTime": t.string().optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1ImportMetadataIn"])
    types["GoogleCloudRecommendationengineV1beta1ImportMetadataOut"] = t.struct(
        {
            "operationName": t.string().optional(),
            "failureCount": t.string().optional(),
            "successCount": t.string().optional(),
            "requestId": t.string().optional(),
            "updateTime": t.string().optional(),
            "createTime": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1ImportMetadataOut"])
    types["GoogleCloudRecommendationengineV1alphaTuningResponseIn"] = t.struct(
        {"_": t.string().optional()}
    ).named(renames["GoogleCloudRecommendationengineV1alphaTuningResponseIn"])
    types["GoogleCloudRecommendationengineV1alphaTuningResponseOut"] = t.struct(
        {"error": t.proxy(renames["ErrorResponse"]).optional()}
    ).named(renames["GoogleCloudRecommendationengineV1alphaTuningResponseOut"])
    types[
        "GoogleCloudRecommendationengineV1beta1ListPredictionApiKeyRegistrationsResponseIn"
    ] = t.struct(
        {
            "nextPageToken": t.string().optional(),
            "predictionApiKeyRegistrations": t.array(
                t.proxy(
                    renames[
                        "GoogleCloudRecommendationengineV1beta1PredictionApiKeyRegistrationIn"
                    ]
                )
            ).optional(),
        }
    ).named(
        renames[
            "GoogleCloudRecommendationengineV1beta1ListPredictionApiKeyRegistrationsResponseIn"
        ]
    )
    types[
        "GoogleCloudRecommendationengineV1beta1ListPredictionApiKeyRegistrationsResponseOut"
    ] = t.struct(
        {
            "nextPageToken": t.string().optional(),
            "predictionApiKeyRegistrations": t.array(
                t.proxy(
                    renames[
                        "GoogleCloudRecommendationengineV1beta1PredictionApiKeyRegistrationOut"
                    ]
                )
            ).optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(
        renames[
            "GoogleCloudRecommendationengineV1beta1ListPredictionApiKeyRegistrationsResponseOut"
        ]
    )
    types["GoogleCloudRecommendationengineV1beta1GcsSourceIn"] = t.struct(
        {"inputUris": t.array(t.string()), "jsonSchema": t.string().optional()}
    ).named(renames["GoogleCloudRecommendationengineV1beta1GcsSourceIn"])
    types["GoogleCloudRecommendationengineV1beta1GcsSourceOut"] = t.struct(
        {
            "inputUris": t.array(t.string()),
            "jsonSchema": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1GcsSourceOut"])
    types["GoogleCloudRecommendationengineV1beta1ListUserEventsResponseIn"] = t.struct(
        {
            "userEvents": t.array(
                t.proxy(renames["GoogleCloudRecommendationengineV1beta1UserEventIn"])
            ).optional(),
            "nextPageToken": t.string().optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1ListUserEventsResponseIn"])
    types["GoogleCloudRecommendationengineV1beta1ListUserEventsResponseOut"] = t.struct(
        {
            "userEvents": t.array(
                t.proxy(renames["GoogleCloudRecommendationengineV1beta1UserEventOut"])
            ).optional(),
            "nextPageToken": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1ListUserEventsResponseOut"])
    types["GoogleCloudRecommendationengineV1beta1ProductCatalogItemIn"] = t.struct(
        {
            "images": t.array(
                t.proxy(renames["GoogleCloudRecommendationengineV1beta1ImageIn"])
            ).optional(),
            "exactPrice": t.proxy(
                renames[
                    "GoogleCloudRecommendationengineV1beta1ProductCatalogItemExactPriceIn"
                ]
            ).optional(),
            "currencyCode": t.string().optional(),
            "canonicalProductUri": t.string().optional(),
            "availableQuantity": t.string().optional(),
            "costs": t.struct({"_": t.string().optional()}).optional(),
            "priceRange": t.proxy(
                renames[
                    "GoogleCloudRecommendationengineV1beta1ProductCatalogItemPriceRangeIn"
                ]
            ).optional(),
            "stockState": t.string().optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1ProductCatalogItemIn"])
    types["GoogleCloudRecommendationengineV1beta1ProductCatalogItemOut"] = t.struct(
        {
            "images": t.array(
                t.proxy(renames["GoogleCloudRecommendationengineV1beta1ImageOut"])
            ).optional(),
            "exactPrice": t.proxy(
                renames[
                    "GoogleCloudRecommendationengineV1beta1ProductCatalogItemExactPriceOut"
                ]
            ).optional(),
            "currencyCode": t.string().optional(),
            "canonicalProductUri": t.string().optional(),
            "availableQuantity": t.string().optional(),
            "costs": t.struct({"_": t.string().optional()}).optional(),
            "priceRange": t.proxy(
                renames[
                    "GoogleCloudRecommendationengineV1beta1ProductCatalogItemPriceRangeOut"
                ]
            ).optional(),
            "stockState": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(renames["GoogleCloudRecommendationengineV1beta1ProductCatalogItemOut"])
    types[
        "GoogleCloudRecommendationengineV1beta1PredictionApiKeyRegistrationIn"
    ] = t.struct({"apiKey": t.string().optional()}).named(
        renames["GoogleCloudRecommendationengineV1beta1PredictionApiKeyRegistrationIn"]
    )
    types[
        "GoogleCloudRecommendationengineV1beta1PredictionApiKeyRegistrationOut"
    ] = t.struct(
        {
            "apiKey": t.string().optional(),
            "error": t.proxy(renames["ErrorResponse"]).optional(),
        }
    ).named(
        renames["GoogleCloudRecommendationengineV1beta1PredictionApiKeyRegistrationOut"]
    )

    functions = {}
    functions["projectsLocationsCatalogsPatch"] = recommendationengine.get(
        "v1beta1/{parent}/catalogs",
        t.struct(
            {
                "pageSize": t.integer().optional(),
                "parent": t.string(),
                "pageToken": t.string().optional(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(
            renames["GoogleCloudRecommendationengineV1beta1ListCatalogsResponseOut"]
        ),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions["projectsLocationsCatalogsList"] = recommendationengine.get(
        "v1beta1/{parent}/catalogs",
        t.struct(
            {
                "pageSize": t.integer().optional(),
                "parent": t.string(),
                "pageToken": t.string().optional(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(
            renames["GoogleCloudRecommendationengineV1beta1ListCatalogsResponseOut"]
        ),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions[
        "projectsLocationsCatalogsEventStoresPlacementsPredict"
    ] = recommendationengine.post(
        "v1beta1/{name}:predict",
        t.struct(
            {
                "name": t.string(),
                "pageToken": t.string().optional(),
                "pageSize": t.integer().optional(),
                "userEvent": t.proxy(
                    renames["GoogleCloudRecommendationengineV1beta1UserEventIn"]
                ),
                "dryRun": t.boolean().optional(),
                "params": t.struct({"_": t.string().optional()}).optional(),
                "labels": t.struct({"_": t.string().optional()}).optional(),
                "filter": t.string().optional(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(renames["GoogleCloudRecommendationengineV1beta1PredictResponseOut"]),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions[
        "projectsLocationsCatalogsEventStoresOperationsList"
    ] = recommendationengine.get(
        "v1beta1/{name}",
        t.struct({"name": t.string().optional(), "auth": t.string().optional()}),
        t.proxy(renames["GoogleLongrunningOperationOut"]),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions[
        "projectsLocationsCatalogsEventStoresOperationsGet"
    ] = recommendationengine.get(
        "v1beta1/{name}",
        t.struct({"name": t.string().optional(), "auth": t.string().optional()}),
        t.proxy(renames["GoogleLongrunningOperationOut"]),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions[
        "projectsLocationsCatalogsEventStoresUserEventsList"
    ] = recommendationengine.post(
        "v1beta1/{parent}/userEvents:purge",
        t.struct(
            {
                "parent": t.string(),
                "filter": t.string(),
                "force": t.boolean().optional(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(renames["GoogleLongrunningOperationOut"]),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions[
        "projectsLocationsCatalogsEventStoresUserEventsCollect"
    ] = recommendationengine.post(
        "v1beta1/{parent}/userEvents:purge",
        t.struct(
            {
                "parent": t.string(),
                "filter": t.string(),
                "force": t.boolean().optional(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(renames["GoogleLongrunningOperationOut"]),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions[
        "projectsLocationsCatalogsEventStoresUserEventsRejoin"
    ] = recommendationengine.post(
        "v1beta1/{parent}/userEvents:purge",
        t.struct(
            {
                "parent": t.string(),
                "filter": t.string(),
                "force": t.boolean().optional(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(renames["GoogleLongrunningOperationOut"]),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions[
        "projectsLocationsCatalogsEventStoresUserEventsWrite"
    ] = recommendationengine.post(
        "v1beta1/{parent}/userEvents:purge",
        t.struct(
            {
                "parent": t.string(),
                "filter": t.string(),
                "force": t.boolean().optional(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(renames["GoogleLongrunningOperationOut"]),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions[
        "projectsLocationsCatalogsEventStoresUserEventsImport"
    ] = recommendationengine.post(
        "v1beta1/{parent}/userEvents:purge",
        t.struct(
            {
                "parent": t.string(),
                "filter": t.string(),
                "force": t.boolean().optional(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(renames["GoogleLongrunningOperationOut"]),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions[
        "projectsLocationsCatalogsEventStoresUserEventsPurge"
    ] = recommendationengine.post(
        "v1beta1/{parent}/userEvents:purge",
        t.struct(
            {
                "parent": t.string(),
                "filter": t.string(),
                "force": t.boolean().optional(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(renames["GoogleLongrunningOperationOut"]),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions[
        "projectsLocationsCatalogsEventStoresPredictionApiKeyRegistrationsDelete"
    ] = recommendationengine.get(
        "v1beta1/{parent}/predictionApiKeyRegistrations",
        t.struct(
            {
                "pageToken": t.string().optional(),
                "parent": t.string(),
                "pageSize": t.integer().optional(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(
            renames[
                "GoogleCloudRecommendationengineV1beta1ListPredictionApiKeyRegistrationsResponseOut"
            ]
        ),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions[
        "projectsLocationsCatalogsEventStoresPredictionApiKeyRegistrationsCreate"
    ] = recommendationengine.get(
        "v1beta1/{parent}/predictionApiKeyRegistrations",
        t.struct(
            {
                "pageToken": t.string().optional(),
                "parent": t.string(),
                "pageSize": t.integer().optional(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(
            renames[
                "GoogleCloudRecommendationengineV1beta1ListPredictionApiKeyRegistrationsResponseOut"
            ]
        ),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions[
        "projectsLocationsCatalogsEventStoresPredictionApiKeyRegistrationsList"
    ] = recommendationengine.get(
        "v1beta1/{parent}/predictionApiKeyRegistrations",
        t.struct(
            {
                "pageToken": t.string().optional(),
                "parent": t.string(),
                "pageSize": t.integer().optional(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(
            renames[
                "GoogleCloudRecommendationengineV1beta1ListPredictionApiKeyRegistrationsResponseOut"
            ]
        ),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions["projectsLocationsCatalogsOperationsGet"] = recommendationengine.get(
        "v1beta1/{name}/operations",
        t.struct(
            {
                "name": t.string().optional(),
                "pageToken": t.string().optional(),
                "pageSize": t.integer().optional(),
                "filter": t.string().optional(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(renames["GoogleLongrunningListOperationsResponseOut"]),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions["projectsLocationsCatalogsOperationsList"] = recommendationengine.get(
        "v1beta1/{name}/operations",
        t.struct(
            {
                "name": t.string().optional(),
                "pageToken": t.string().optional(),
                "pageSize": t.integer().optional(),
                "filter": t.string().optional(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(renames["GoogleLongrunningListOperationsResponseOut"]),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions["projectsLocationsCatalogsCatalogItemsGet"] = recommendationengine.patch(
        "v1beta1/{name}",
        t.struct(
            {
                "name": t.string(),
                "updateMask": t.string().optional(),
                "categoryHierarchies": t.array(
                    t.proxy(
                        renames[
                            "GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyIn"
                        ]
                    )
                ),
                "id": t.string(),
                "itemAttributes": t.proxy(
                    renames["GoogleCloudRecommendationengineV1beta1FeatureMapIn"]
                ).optional(),
                "languageCode": t.string().optional(),
                "description": t.string().optional(),
                "productMetadata": t.proxy(
                    renames[
                        "GoogleCloudRecommendationengineV1beta1ProductCatalogItemIn"
                    ]
                ).optional(),
                "tags": t.array(t.string()).optional(),
                "itemGroupId": t.string().optional(),
                "title": t.string(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(renames["GoogleCloudRecommendationengineV1beta1CatalogItemOut"]),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions[
        "projectsLocationsCatalogsCatalogItemsImport"
    ] = recommendationengine.patch(
        "v1beta1/{name}",
        t.struct(
            {
                "name": t.string(),
                "updateMask": t.string().optional(),
                "categoryHierarchies": t.array(
                    t.proxy(
                        renames[
                            "GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyIn"
                        ]
                    )
                ),
                "id": t.string(),
                "itemAttributes": t.proxy(
                    renames["GoogleCloudRecommendationengineV1beta1FeatureMapIn"]
                ).optional(),
                "languageCode": t.string().optional(),
                "description": t.string().optional(),
                "productMetadata": t.proxy(
                    renames[
                        "GoogleCloudRecommendationengineV1beta1ProductCatalogItemIn"
                    ]
                ).optional(),
                "tags": t.array(t.string()).optional(),
                "itemGroupId": t.string().optional(),
                "title": t.string(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(renames["GoogleCloudRecommendationengineV1beta1CatalogItemOut"]),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions["projectsLocationsCatalogsCatalogItemsList"] = recommendationengine.patch(
        "v1beta1/{name}",
        t.struct(
            {
                "name": t.string(),
                "updateMask": t.string().optional(),
                "categoryHierarchies": t.array(
                    t.proxy(
                        renames[
                            "GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyIn"
                        ]
                    )
                ),
                "id": t.string(),
                "itemAttributes": t.proxy(
                    renames["GoogleCloudRecommendationengineV1beta1FeatureMapIn"]
                ).optional(),
                "languageCode": t.string().optional(),
                "description": t.string().optional(),
                "productMetadata": t.proxy(
                    renames[
                        "GoogleCloudRecommendationengineV1beta1ProductCatalogItemIn"
                    ]
                ).optional(),
                "tags": t.array(t.string()).optional(),
                "itemGroupId": t.string().optional(),
                "title": t.string(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(renames["GoogleCloudRecommendationengineV1beta1CatalogItemOut"]),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions[
        "projectsLocationsCatalogsCatalogItemsDelete"
    ] = recommendationengine.patch(
        "v1beta1/{name}",
        t.struct(
            {
                "name": t.string(),
                "updateMask": t.string().optional(),
                "categoryHierarchies": t.array(
                    t.proxy(
                        renames[
                            "GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyIn"
                        ]
                    )
                ),
                "id": t.string(),
                "itemAttributes": t.proxy(
                    renames["GoogleCloudRecommendationengineV1beta1FeatureMapIn"]
                ).optional(),
                "languageCode": t.string().optional(),
                "description": t.string().optional(),
                "productMetadata": t.proxy(
                    renames[
                        "GoogleCloudRecommendationengineV1beta1ProductCatalogItemIn"
                    ]
                ).optional(),
                "tags": t.array(t.string()).optional(),
                "itemGroupId": t.string().optional(),
                "title": t.string(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(renames["GoogleCloudRecommendationengineV1beta1CatalogItemOut"]),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions[
        "projectsLocationsCatalogsCatalogItemsCreate"
    ] = recommendationengine.patch(
        "v1beta1/{name}",
        t.struct(
            {
                "name": t.string(),
                "updateMask": t.string().optional(),
                "categoryHierarchies": t.array(
                    t.proxy(
                        renames[
                            "GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyIn"
                        ]
                    )
                ),
                "id": t.string(),
                "itemAttributes": t.proxy(
                    renames["GoogleCloudRecommendationengineV1beta1FeatureMapIn"]
                ).optional(),
                "languageCode": t.string().optional(),
                "description": t.string().optional(),
                "productMetadata": t.proxy(
                    renames[
                        "GoogleCloudRecommendationengineV1beta1ProductCatalogItemIn"
                    ]
                ).optional(),
                "tags": t.array(t.string()).optional(),
                "itemGroupId": t.string().optional(),
                "title": t.string(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(renames["GoogleCloudRecommendationengineV1beta1CatalogItemOut"]),
        auth_token_field="auth",
        content_type="application/json",
    )
    functions[
        "projectsLocationsCatalogsCatalogItemsPatch"
    ] = recommendationengine.patch(
        "v1beta1/{name}",
        t.struct(
            {
                "name": t.string(),
                "updateMask": t.string().optional(),
                "categoryHierarchies": t.array(
                    t.proxy(
                        renames[
                            "GoogleCloudRecommendationengineV1beta1CatalogItemCategoryHierarchyIn"
                        ]
                    )
                ),
                "id": t.string(),
                "itemAttributes": t.proxy(
                    renames["GoogleCloudRecommendationengineV1beta1FeatureMapIn"]
                ).optional(),
                "languageCode": t.string().optional(),
                "description": t.string().optional(),
                "productMetadata": t.proxy(
                    renames[
                        "GoogleCloudRecommendationengineV1beta1ProductCatalogItemIn"
                    ]
                ).optional(),
                "tags": t.array(t.string()).optional(),
                "itemGroupId": t.string().optional(),
                "title": t.string(),
                "auth": t.string().optional(),
            }
        ),
        t.proxy(renames["GoogleCloudRecommendationengineV1beta1CatalogItemOut"]),
        auth_token_field="auth",
        content_type="application/json",
    )

    return Import(
        importer="recommendationengine",
        renames=renames,
        types=Box(types),
        functions=Box(functions),
    )
