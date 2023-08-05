# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from gooddata_metadata_client.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from gooddata_metadata_client.model.assignee_identifier import AssigneeIdentifier
from gooddata_metadata_client.model.data_source_table_identifier import DataSourceTableIdentifier
from gooddata_metadata_client.model.dataset_reference_identifier import DatasetReferenceIdentifier
from gooddata_metadata_client.model.declarative_analytical_dashboard import DeclarativeAnalyticalDashboard
from gooddata_metadata_client.model.declarative_analytics import DeclarativeAnalytics
from gooddata_metadata_client.model.declarative_analytics_layer import DeclarativeAnalyticsLayer
from gooddata_metadata_client.model.declarative_attribute import DeclarativeAttribute
from gooddata_metadata_client.model.declarative_column import DeclarativeColumn
from gooddata_metadata_client.model.declarative_dashboard_plugin import DeclarativeDashboardPlugin
from gooddata_metadata_client.model.declarative_data_source import DeclarativeDataSource
from gooddata_metadata_client.model.declarative_data_source_permission import DeclarativeDataSourcePermission
from gooddata_metadata_client.model.declarative_data_sources import DeclarativeDataSources
from gooddata_metadata_client.model.declarative_dataset import DeclarativeDataset
from gooddata_metadata_client.model.declarative_date_dataset import DeclarativeDateDataset
from gooddata_metadata_client.model.declarative_fact import DeclarativeFact
from gooddata_metadata_client.model.declarative_filter_context import DeclarativeFilterContext
from gooddata_metadata_client.model.declarative_label import DeclarativeLabel
from gooddata_metadata_client.model.declarative_ldm import DeclarativeLdm
from gooddata_metadata_client.model.declarative_metric import DeclarativeMetric
from gooddata_metadata_client.model.declarative_model import DeclarativeModel
from gooddata_metadata_client.model.declarative_organization import DeclarativeOrganization
from gooddata_metadata_client.model.declarative_organization_info import DeclarativeOrganizationInfo
from gooddata_metadata_client.model.declarative_organization_permission import DeclarativeOrganizationPermission
from gooddata_metadata_client.model.declarative_pdm import DeclarativePdm
from gooddata_metadata_client.model.declarative_reference import DeclarativeReference
from gooddata_metadata_client.model.declarative_single_workspace_permission import DeclarativeSingleWorkspacePermission
from gooddata_metadata_client.model.declarative_table import DeclarativeTable
from gooddata_metadata_client.model.declarative_tables import DeclarativeTables
from gooddata_metadata_client.model.declarative_user import DeclarativeUser
from gooddata_metadata_client.model.declarative_user_group import DeclarativeUserGroup
from gooddata_metadata_client.model.declarative_user_groups import DeclarativeUserGroups
from gooddata_metadata_client.model.declarative_users import DeclarativeUsers
from gooddata_metadata_client.model.declarative_users_user_groups import DeclarativeUsersUserGroups
from gooddata_metadata_client.model.declarative_visualization_object import DeclarativeVisualizationObject
from gooddata_metadata_client.model.declarative_workspace import DeclarativeWorkspace
from gooddata_metadata_client.model.declarative_workspace_data_filter import DeclarativeWorkspaceDataFilter
from gooddata_metadata_client.model.declarative_workspace_data_filter_setting import DeclarativeWorkspaceDataFilterSetting
from gooddata_metadata_client.model.declarative_workspace_data_filters import DeclarativeWorkspaceDataFilters
from gooddata_metadata_client.model.declarative_workspace_hierarchy_permission import DeclarativeWorkspaceHierarchyPermission
from gooddata_metadata_client.model.declarative_workspace_model import DeclarativeWorkspaceModel
from gooddata_metadata_client.model.declarative_workspace_permissions import DeclarativeWorkspacePermissions
from gooddata_metadata_client.model.declarative_workspaces import DeclarativeWorkspaces
from gooddata_metadata_client.model.generate_ldm_request import GenerateLdmRequest
from gooddata_metadata_client.model.grain_identifier import GrainIdentifier
from gooddata_metadata_client.model.granularities_formatting import GranularitiesFormatting
from gooddata_metadata_client.model.inline_response200 import InlineResponse200
from gooddata_metadata_client.model.inline_response200_options import InlineResponse200Options
from gooddata_metadata_client.model.inline_response200_options_links import InlineResponse200OptionsLinks
from gooddata_metadata_client.model.json_api_analytical_dashboard_in import JsonApiAnalyticalDashboardIn
from gooddata_metadata_client.model.json_api_analytical_dashboard_in_attributes import JsonApiAnalyticalDashboardInAttributes
from gooddata_metadata_client.model.json_api_analytical_dashboard_in_document import JsonApiAnalyticalDashboardInDocument
from gooddata_metadata_client.model.json_api_analytical_dashboard_linkage import JsonApiAnalyticalDashboardLinkage
from gooddata_metadata_client.model.json_api_analytical_dashboard_out import JsonApiAnalyticalDashboardOut
from gooddata_metadata_client.model.json_api_analytical_dashboard_out_document import JsonApiAnalyticalDashboardOutDocument
from gooddata_metadata_client.model.json_api_analytical_dashboard_out_includes import JsonApiAnalyticalDashboardOutIncludes
from gooddata_metadata_client.model.json_api_analytical_dashboard_out_list import JsonApiAnalyticalDashboardOutList
from gooddata_metadata_client.model.json_api_analytical_dashboard_out_relationships import JsonApiAnalyticalDashboardOutRelationships
from gooddata_metadata_client.model.json_api_analytical_dashboard_out_relationships_analytical_dashboards import JsonApiAnalyticalDashboardOutRelationshipsAnalyticalDashboards
from gooddata_metadata_client.model.json_api_analytical_dashboard_out_relationships_dashboard_plugins import JsonApiAnalyticalDashboardOutRelationshipsDashboardPlugins
from gooddata_metadata_client.model.json_api_analytical_dashboard_out_relationships_datasets import JsonApiAnalyticalDashboardOutRelationshipsDatasets
from gooddata_metadata_client.model.json_api_analytical_dashboard_out_relationships_filter_contexts import JsonApiAnalyticalDashboardOutRelationshipsFilterContexts
from gooddata_metadata_client.model.json_api_analytical_dashboard_out_relationships_labels import JsonApiAnalyticalDashboardOutRelationshipsLabels
from gooddata_metadata_client.model.json_api_analytical_dashboard_out_relationships_metrics import JsonApiAnalyticalDashboardOutRelationshipsMetrics
from gooddata_metadata_client.model.json_api_analytical_dashboard_out_relationships_visualization_objects import JsonApiAnalyticalDashboardOutRelationshipsVisualizationObjects
from gooddata_metadata_client.model.json_api_analytical_dashboard_out_with_links import JsonApiAnalyticalDashboardOutWithLinks
from gooddata_metadata_client.model.json_api_analytical_dashboard_patch import JsonApiAnalyticalDashboardPatch
from gooddata_metadata_client.model.json_api_analytical_dashboard_patch_document import JsonApiAnalyticalDashboardPatchDocument
from gooddata_metadata_client.model.json_api_analytical_dashboard_to_many_linkage import JsonApiAnalyticalDashboardToManyLinkage
from gooddata_metadata_client.model.json_api_api_token_in import JsonApiApiTokenIn
from gooddata_metadata_client.model.json_api_api_token_in_document import JsonApiApiTokenInDocument
from gooddata_metadata_client.model.json_api_api_token_out import JsonApiApiTokenOut
from gooddata_metadata_client.model.json_api_api_token_out_attributes import JsonApiApiTokenOutAttributes
from gooddata_metadata_client.model.json_api_api_token_out_document import JsonApiApiTokenOutDocument
from gooddata_metadata_client.model.json_api_api_token_out_list import JsonApiApiTokenOutList
from gooddata_metadata_client.model.json_api_api_token_out_with_links import JsonApiApiTokenOutWithLinks
from gooddata_metadata_client.model.json_api_attribute_linkage import JsonApiAttributeLinkage
from gooddata_metadata_client.model.json_api_attribute_out import JsonApiAttributeOut
from gooddata_metadata_client.model.json_api_attribute_out_attributes import JsonApiAttributeOutAttributes
from gooddata_metadata_client.model.json_api_attribute_out_document import JsonApiAttributeOutDocument
from gooddata_metadata_client.model.json_api_attribute_out_includes import JsonApiAttributeOutIncludes
from gooddata_metadata_client.model.json_api_attribute_out_list import JsonApiAttributeOutList
from gooddata_metadata_client.model.json_api_attribute_out_relationships import JsonApiAttributeOutRelationships
from gooddata_metadata_client.model.json_api_attribute_out_relationships_dataset import JsonApiAttributeOutRelationshipsDataset
from gooddata_metadata_client.model.json_api_attribute_out_with_links import JsonApiAttributeOutWithLinks
from gooddata_metadata_client.model.json_api_attribute_to_many_linkage import JsonApiAttributeToManyLinkage
from gooddata_metadata_client.model.json_api_attribute_to_one_linkage import JsonApiAttributeToOneLinkage
from gooddata_metadata_client.model.json_api_cookie_security_configuration_in import JsonApiCookieSecurityConfigurationIn
from gooddata_metadata_client.model.json_api_cookie_security_configuration_in_document import JsonApiCookieSecurityConfigurationInDocument
from gooddata_metadata_client.model.json_api_cookie_security_configuration_out import JsonApiCookieSecurityConfigurationOut
from gooddata_metadata_client.model.json_api_cookie_security_configuration_out_attributes import JsonApiCookieSecurityConfigurationOutAttributes
from gooddata_metadata_client.model.json_api_cookie_security_configuration_out_document import JsonApiCookieSecurityConfigurationOutDocument
from gooddata_metadata_client.model.json_api_dashboard_plugin_in import JsonApiDashboardPluginIn
from gooddata_metadata_client.model.json_api_dashboard_plugin_in_attributes import JsonApiDashboardPluginInAttributes
from gooddata_metadata_client.model.json_api_dashboard_plugin_in_document import JsonApiDashboardPluginInDocument
from gooddata_metadata_client.model.json_api_dashboard_plugin_linkage import JsonApiDashboardPluginLinkage
from gooddata_metadata_client.model.json_api_dashboard_plugin_out import JsonApiDashboardPluginOut
from gooddata_metadata_client.model.json_api_dashboard_plugin_out_document import JsonApiDashboardPluginOutDocument
from gooddata_metadata_client.model.json_api_dashboard_plugin_out_list import JsonApiDashboardPluginOutList
from gooddata_metadata_client.model.json_api_dashboard_plugin_out_with_links import JsonApiDashboardPluginOutWithLinks
from gooddata_metadata_client.model.json_api_dashboard_plugin_patch import JsonApiDashboardPluginPatch
from gooddata_metadata_client.model.json_api_dashboard_plugin_patch_document import JsonApiDashboardPluginPatchDocument
from gooddata_metadata_client.model.json_api_dashboard_plugin_to_many_linkage import JsonApiDashboardPluginToManyLinkage
from gooddata_metadata_client.model.json_api_data_source_identifier_out import JsonApiDataSourceIdentifierOut
from gooddata_metadata_client.model.json_api_data_source_identifier_out_attributes import JsonApiDataSourceIdentifierOutAttributes
from gooddata_metadata_client.model.json_api_data_source_identifier_out_document import JsonApiDataSourceIdentifierOutDocument
from gooddata_metadata_client.model.json_api_data_source_identifier_out_list import JsonApiDataSourceIdentifierOutList
from gooddata_metadata_client.model.json_api_data_source_identifier_out_with_links import JsonApiDataSourceIdentifierOutWithLinks
from gooddata_metadata_client.model.json_api_data_source_in import JsonApiDataSourceIn
from gooddata_metadata_client.model.json_api_data_source_in_attributes import JsonApiDataSourceInAttributes
from gooddata_metadata_client.model.json_api_data_source_in_document import JsonApiDataSourceInDocument
from gooddata_metadata_client.model.json_api_data_source_out import JsonApiDataSourceOut
from gooddata_metadata_client.model.json_api_data_source_out_attributes import JsonApiDataSourceOutAttributes
from gooddata_metadata_client.model.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from gooddata_metadata_client.model.json_api_data_source_out_list import JsonApiDataSourceOutList
from gooddata_metadata_client.model.json_api_data_source_out_meta import JsonApiDataSourceOutMeta
from gooddata_metadata_client.model.json_api_data_source_out_with_links import JsonApiDataSourceOutWithLinks
from gooddata_metadata_client.model.json_api_data_source_patch import JsonApiDataSourcePatch
from gooddata_metadata_client.model.json_api_data_source_patch_attributes import JsonApiDataSourcePatchAttributes
from gooddata_metadata_client.model.json_api_data_source_patch_document import JsonApiDataSourcePatchDocument
from gooddata_metadata_client.model.json_api_data_source_table_out import JsonApiDataSourceTableOut
from gooddata_metadata_client.model.json_api_data_source_table_out_attributes import JsonApiDataSourceTableOutAttributes
from gooddata_metadata_client.model.json_api_data_source_table_out_attributes_columns import JsonApiDataSourceTableOutAttributesColumns
from gooddata_metadata_client.model.json_api_data_source_table_out_document import JsonApiDataSourceTableOutDocument
from gooddata_metadata_client.model.json_api_data_source_table_out_list import JsonApiDataSourceTableOutList
from gooddata_metadata_client.model.json_api_data_source_table_out_with_links import JsonApiDataSourceTableOutWithLinks
from gooddata_metadata_client.model.json_api_dataset_linkage import JsonApiDatasetLinkage
from gooddata_metadata_client.model.json_api_dataset_out import JsonApiDatasetOut
from gooddata_metadata_client.model.json_api_dataset_out_attributes import JsonApiDatasetOutAttributes
from gooddata_metadata_client.model.json_api_dataset_out_attributes_grain import JsonApiDatasetOutAttributesGrain
from gooddata_metadata_client.model.json_api_dataset_out_attributes_reference_properties import JsonApiDatasetOutAttributesReferenceProperties
from gooddata_metadata_client.model.json_api_dataset_out_document import JsonApiDatasetOutDocument
from gooddata_metadata_client.model.json_api_dataset_out_includes import JsonApiDatasetOutIncludes
from gooddata_metadata_client.model.json_api_dataset_out_list import JsonApiDatasetOutList
from gooddata_metadata_client.model.json_api_dataset_out_relationships import JsonApiDatasetOutRelationships
from gooddata_metadata_client.model.json_api_dataset_out_with_links import JsonApiDatasetOutWithLinks
from gooddata_metadata_client.model.json_api_dataset_to_many_linkage import JsonApiDatasetToManyLinkage
from gooddata_metadata_client.model.json_api_dataset_to_one_linkage import JsonApiDatasetToOneLinkage
from gooddata_metadata_client.model.json_api_fact_linkage import JsonApiFactLinkage
from gooddata_metadata_client.model.json_api_fact_out import JsonApiFactOut
from gooddata_metadata_client.model.json_api_fact_out_attributes import JsonApiFactOutAttributes
from gooddata_metadata_client.model.json_api_fact_out_document import JsonApiFactOutDocument
from gooddata_metadata_client.model.json_api_fact_out_list import JsonApiFactOutList
from gooddata_metadata_client.model.json_api_fact_out_relationships import JsonApiFactOutRelationships
from gooddata_metadata_client.model.json_api_fact_out_with_links import JsonApiFactOutWithLinks
from gooddata_metadata_client.model.json_api_fact_to_many_linkage import JsonApiFactToManyLinkage
from gooddata_metadata_client.model.json_api_filter_context_in import JsonApiFilterContextIn
from gooddata_metadata_client.model.json_api_filter_context_in_document import JsonApiFilterContextInDocument
from gooddata_metadata_client.model.json_api_filter_context_linkage import JsonApiFilterContextLinkage
from gooddata_metadata_client.model.json_api_filter_context_out import JsonApiFilterContextOut
from gooddata_metadata_client.model.json_api_filter_context_out_document import JsonApiFilterContextOutDocument
from gooddata_metadata_client.model.json_api_filter_context_out_includes import JsonApiFilterContextOutIncludes
from gooddata_metadata_client.model.json_api_filter_context_out_list import JsonApiFilterContextOutList
from gooddata_metadata_client.model.json_api_filter_context_out_relationships import JsonApiFilterContextOutRelationships
from gooddata_metadata_client.model.json_api_filter_context_out_relationships_attributes import JsonApiFilterContextOutRelationshipsAttributes
from gooddata_metadata_client.model.json_api_filter_context_out_with_links import JsonApiFilterContextOutWithLinks
from gooddata_metadata_client.model.json_api_filter_context_patch import JsonApiFilterContextPatch
from gooddata_metadata_client.model.json_api_filter_context_patch_document import JsonApiFilterContextPatchDocument
from gooddata_metadata_client.model.json_api_filter_context_to_many_linkage import JsonApiFilterContextToManyLinkage
from gooddata_metadata_client.model.json_api_label_linkage import JsonApiLabelLinkage
from gooddata_metadata_client.model.json_api_label_out import JsonApiLabelOut
from gooddata_metadata_client.model.json_api_label_out_attributes import JsonApiLabelOutAttributes
from gooddata_metadata_client.model.json_api_label_out_document import JsonApiLabelOutDocument
from gooddata_metadata_client.model.json_api_label_out_list import JsonApiLabelOutList
from gooddata_metadata_client.model.json_api_label_out_relationships import JsonApiLabelOutRelationships
from gooddata_metadata_client.model.json_api_label_out_relationships_attribute import JsonApiLabelOutRelationshipsAttribute
from gooddata_metadata_client.model.json_api_label_out_with_links import JsonApiLabelOutWithLinks
from gooddata_metadata_client.model.json_api_label_to_many_linkage import JsonApiLabelToManyLinkage
from gooddata_metadata_client.model.json_api_metric_in import JsonApiMetricIn
from gooddata_metadata_client.model.json_api_metric_in_attributes import JsonApiMetricInAttributes
from gooddata_metadata_client.model.json_api_metric_in_attributes_content import JsonApiMetricInAttributesContent
from gooddata_metadata_client.model.json_api_metric_in_document import JsonApiMetricInDocument
from gooddata_metadata_client.model.json_api_metric_linkage import JsonApiMetricLinkage
from gooddata_metadata_client.model.json_api_metric_out import JsonApiMetricOut
from gooddata_metadata_client.model.json_api_metric_out_document import JsonApiMetricOutDocument
from gooddata_metadata_client.model.json_api_metric_out_includes import JsonApiMetricOutIncludes
from gooddata_metadata_client.model.json_api_metric_out_list import JsonApiMetricOutList
from gooddata_metadata_client.model.json_api_metric_out_relationships import JsonApiMetricOutRelationships
from gooddata_metadata_client.model.json_api_metric_out_relationships_facts import JsonApiMetricOutRelationshipsFacts
from gooddata_metadata_client.model.json_api_metric_out_with_links import JsonApiMetricOutWithLinks
from gooddata_metadata_client.model.json_api_metric_patch import JsonApiMetricPatch
from gooddata_metadata_client.model.json_api_metric_patch_attributes import JsonApiMetricPatchAttributes
from gooddata_metadata_client.model.json_api_metric_patch_document import JsonApiMetricPatchDocument
from gooddata_metadata_client.model.json_api_metric_to_many_linkage import JsonApiMetricToManyLinkage
from gooddata_metadata_client.model.json_api_organization_in import JsonApiOrganizationIn
from gooddata_metadata_client.model.json_api_organization_in_attributes import JsonApiOrganizationInAttributes
from gooddata_metadata_client.model.json_api_organization_in_document import JsonApiOrganizationInDocument
from gooddata_metadata_client.model.json_api_organization_out import JsonApiOrganizationOut
from gooddata_metadata_client.model.json_api_organization_out_attributes import JsonApiOrganizationOutAttributes
from gooddata_metadata_client.model.json_api_organization_out_document import JsonApiOrganizationOutDocument
from gooddata_metadata_client.model.json_api_organization_out_includes import JsonApiOrganizationOutIncludes
from gooddata_metadata_client.model.json_api_organization_out_meta import JsonApiOrganizationOutMeta
from gooddata_metadata_client.model.json_api_organization_out_relationships import JsonApiOrganizationOutRelationships
from gooddata_metadata_client.model.json_api_organization_out_relationships_bootstrap_user import JsonApiOrganizationOutRelationshipsBootstrapUser
from gooddata_metadata_client.model.json_api_organization_out_relationships_bootstrap_user_group import JsonApiOrganizationOutRelationshipsBootstrapUserGroup
from gooddata_metadata_client.model.json_api_user_group_in import JsonApiUserGroupIn
from gooddata_metadata_client.model.json_api_user_group_in_document import JsonApiUserGroupInDocument
from gooddata_metadata_client.model.json_api_user_group_in_relationships import JsonApiUserGroupInRelationships
from gooddata_metadata_client.model.json_api_user_group_in_relationships_parents import JsonApiUserGroupInRelationshipsParents
from gooddata_metadata_client.model.json_api_user_group_linkage import JsonApiUserGroupLinkage
from gooddata_metadata_client.model.json_api_user_group_out import JsonApiUserGroupOut
from gooddata_metadata_client.model.json_api_user_group_out_document import JsonApiUserGroupOutDocument
from gooddata_metadata_client.model.json_api_user_group_out_list import JsonApiUserGroupOutList
from gooddata_metadata_client.model.json_api_user_group_out_with_links import JsonApiUserGroupOutWithLinks
from gooddata_metadata_client.model.json_api_user_group_patch import JsonApiUserGroupPatch
from gooddata_metadata_client.model.json_api_user_group_patch_document import JsonApiUserGroupPatchDocument
from gooddata_metadata_client.model.json_api_user_group_to_many_linkage import JsonApiUserGroupToManyLinkage
from gooddata_metadata_client.model.json_api_user_group_to_one_linkage import JsonApiUserGroupToOneLinkage
from gooddata_metadata_client.model.json_api_user_in import JsonApiUserIn
from gooddata_metadata_client.model.json_api_user_in_attributes import JsonApiUserInAttributes
from gooddata_metadata_client.model.json_api_user_in_document import JsonApiUserInDocument
from gooddata_metadata_client.model.json_api_user_in_relationships import JsonApiUserInRelationships
from gooddata_metadata_client.model.json_api_user_linkage import JsonApiUserLinkage
from gooddata_metadata_client.model.json_api_user_out import JsonApiUserOut
from gooddata_metadata_client.model.json_api_user_out_document import JsonApiUserOutDocument
from gooddata_metadata_client.model.json_api_user_out_list import JsonApiUserOutList
from gooddata_metadata_client.model.json_api_user_out_with_links import JsonApiUserOutWithLinks
from gooddata_metadata_client.model.json_api_user_patch import JsonApiUserPatch
from gooddata_metadata_client.model.json_api_user_patch_document import JsonApiUserPatchDocument
from gooddata_metadata_client.model.json_api_user_to_one_linkage import JsonApiUserToOneLinkage
from gooddata_metadata_client.model.json_api_visualization_object_in import JsonApiVisualizationObjectIn
from gooddata_metadata_client.model.json_api_visualization_object_in_document import JsonApiVisualizationObjectInDocument
from gooddata_metadata_client.model.json_api_visualization_object_linkage import JsonApiVisualizationObjectLinkage
from gooddata_metadata_client.model.json_api_visualization_object_out import JsonApiVisualizationObjectOut
from gooddata_metadata_client.model.json_api_visualization_object_out_document import JsonApiVisualizationObjectOutDocument
from gooddata_metadata_client.model.json_api_visualization_object_out_includes import JsonApiVisualizationObjectOutIncludes
from gooddata_metadata_client.model.json_api_visualization_object_out_list import JsonApiVisualizationObjectOutList
from gooddata_metadata_client.model.json_api_visualization_object_out_relationships import JsonApiVisualizationObjectOutRelationships
from gooddata_metadata_client.model.json_api_visualization_object_out_with_links import JsonApiVisualizationObjectOutWithLinks
from gooddata_metadata_client.model.json_api_visualization_object_patch import JsonApiVisualizationObjectPatch
from gooddata_metadata_client.model.json_api_visualization_object_patch_document import JsonApiVisualizationObjectPatchDocument
from gooddata_metadata_client.model.json_api_visualization_object_to_many_linkage import JsonApiVisualizationObjectToManyLinkage
from gooddata_metadata_client.model.json_api_workspace_data_filter_in import JsonApiWorkspaceDataFilterIn
from gooddata_metadata_client.model.json_api_workspace_data_filter_in_attributes import JsonApiWorkspaceDataFilterInAttributes
from gooddata_metadata_client.model.json_api_workspace_data_filter_in_document import JsonApiWorkspaceDataFilterInDocument
from gooddata_metadata_client.model.json_api_workspace_data_filter_in_relationships import JsonApiWorkspaceDataFilterInRelationships
from gooddata_metadata_client.model.json_api_workspace_data_filter_in_relationships_filter_settings import JsonApiWorkspaceDataFilterInRelationshipsFilterSettings
from gooddata_metadata_client.model.json_api_workspace_data_filter_linkage import JsonApiWorkspaceDataFilterLinkage
from gooddata_metadata_client.model.json_api_workspace_data_filter_out import JsonApiWorkspaceDataFilterOut
from gooddata_metadata_client.model.json_api_workspace_data_filter_out_document import JsonApiWorkspaceDataFilterOutDocument
from gooddata_metadata_client.model.json_api_workspace_data_filter_out_list import JsonApiWorkspaceDataFilterOutList
from gooddata_metadata_client.model.json_api_workspace_data_filter_out_with_links import JsonApiWorkspaceDataFilterOutWithLinks
from gooddata_metadata_client.model.json_api_workspace_data_filter_patch import JsonApiWorkspaceDataFilterPatch
from gooddata_metadata_client.model.json_api_workspace_data_filter_patch_document import JsonApiWorkspaceDataFilterPatchDocument
from gooddata_metadata_client.model.json_api_workspace_data_filter_setting_linkage import JsonApiWorkspaceDataFilterSettingLinkage
from gooddata_metadata_client.model.json_api_workspace_data_filter_setting_out import JsonApiWorkspaceDataFilterSettingOut
from gooddata_metadata_client.model.json_api_workspace_data_filter_setting_out_attributes import JsonApiWorkspaceDataFilterSettingOutAttributes
from gooddata_metadata_client.model.json_api_workspace_data_filter_setting_out_document import JsonApiWorkspaceDataFilterSettingOutDocument
from gooddata_metadata_client.model.json_api_workspace_data_filter_setting_out_list import JsonApiWorkspaceDataFilterSettingOutList
from gooddata_metadata_client.model.json_api_workspace_data_filter_setting_out_relationships import JsonApiWorkspaceDataFilterSettingOutRelationships
from gooddata_metadata_client.model.json_api_workspace_data_filter_setting_out_relationships_workspace_data_filter import JsonApiWorkspaceDataFilterSettingOutRelationshipsWorkspaceDataFilter
from gooddata_metadata_client.model.json_api_workspace_data_filter_setting_out_with_links import JsonApiWorkspaceDataFilterSettingOutWithLinks
from gooddata_metadata_client.model.json_api_workspace_data_filter_setting_to_many_linkage import JsonApiWorkspaceDataFilterSettingToManyLinkage
from gooddata_metadata_client.model.json_api_workspace_data_filter_to_one_linkage import JsonApiWorkspaceDataFilterToOneLinkage
from gooddata_metadata_client.model.json_api_workspace_in import JsonApiWorkspaceIn
from gooddata_metadata_client.model.json_api_workspace_in_attributes import JsonApiWorkspaceInAttributes
from gooddata_metadata_client.model.json_api_workspace_in_document import JsonApiWorkspaceInDocument
from gooddata_metadata_client.model.json_api_workspace_in_relationships import JsonApiWorkspaceInRelationships
from gooddata_metadata_client.model.json_api_workspace_in_relationships_parent import JsonApiWorkspaceInRelationshipsParent
from gooddata_metadata_client.model.json_api_workspace_linkage import JsonApiWorkspaceLinkage
from gooddata_metadata_client.model.json_api_workspace_out import JsonApiWorkspaceOut
from gooddata_metadata_client.model.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
from gooddata_metadata_client.model.json_api_workspace_out_list import JsonApiWorkspaceOutList
from gooddata_metadata_client.model.json_api_workspace_out_meta import JsonApiWorkspaceOutMeta
from gooddata_metadata_client.model.json_api_workspace_out_meta_config import JsonApiWorkspaceOutMetaConfig
from gooddata_metadata_client.model.json_api_workspace_out_with_links import JsonApiWorkspaceOutWithLinks
from gooddata_metadata_client.model.json_api_workspace_patch import JsonApiWorkspacePatch
from gooddata_metadata_client.model.json_api_workspace_patch_document import JsonApiWorkspacePatchDocument
from gooddata_metadata_client.model.json_api_workspace_to_one_linkage import JsonApiWorkspaceToOneLinkage
from gooddata_metadata_client.model.list_links import ListLinks
from gooddata_metadata_client.model.list_links_all_of import ListLinksAllOf
from gooddata_metadata_client.model.object_links import ObjectLinks
from gooddata_metadata_client.model.object_links_container import ObjectLinksContainer
from gooddata_metadata_client.model.reference_identifier import ReferenceIdentifier
from gooddata_metadata_client.model.user_group_identifier import UserGroupIdentifier
from gooddata_metadata_client.model.workspace_identifier import WorkspaceIdentifier
