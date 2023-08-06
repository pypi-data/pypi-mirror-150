from infoworks.sdk.source_client import SourceClient
from infoworks.sdk.pipeline_client import PipelineClient
from infoworks.sdk.workflow_client import WorkflowClient
from infoworks.sdk.domain_client import DomainClient
from infoworks.sdk.jobmetrics import JobMetricsClient
from infoworks.sdk.admin_client import AdminClient
import logging


class InfoworksClientSDK(SourceClient, PipelineClient, WorkflowClient, DomainClient, AdminClient, JobMetricsClient):
    def __init__(self):
        try:
            SourceClient.__init__(self)
            PipelineClient.__init__(self)
            WorkflowClient.__init__(self)
            DomainClient.__init__(self)
            AdminClient.__init__(self)
            JobMetricsClient.__init__(self)
        except Exception as e:
            logging.info(e)
