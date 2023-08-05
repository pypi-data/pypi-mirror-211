from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField, RelationsField
from invenio_records_resources.records.api import Record
from invenio_records_resources.records.systemfields import IndexField
from invenio_records_resources.records.systemfields.pid import PIDField, PIDFieldContext
from invenio_vocabularies.records.api import Vocabulary
from oarepo_runtime.relations import PIDRelation, RelationsField

from nr_metadata.documents.records.dumper import DocumentsDumper
from nr_metadata.documents.records.models import DocumentsMetadata
from nr_metadata.documents.records.multilingual_dumper import MultilingualDumper


class DocumentsIdProvider(RecordIdProviderV2):
    pid_type = "dcmnts"


class DocumentsRecord(Record):
    model_cls = DocumentsMetadata

    schema = ConstantField("$schema", "local://documents-1.0.0.json")

    index = IndexField("documents-documents-1.0.0")

    pid = PIDField(
        provider=DocumentsIdProvider, context_cls=PIDFieldContext, create=True
    )

    dumper_extensions = [MultilingualDumper()]
    dumper = DocumentsDumper(extensions=dumper_extensions)

    relations = RelationsField(
        degreeGrantors_item=PIDRelation(
            "metadata.thesis.degreeGrantors",
            keys=["id", "title", {"key": "type.id", "target": "type"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        affiliations_item=PIDRelation(
            "metadata.creators.affiliations",
            keys=["id", "title", {"key": "type.id", "target": "type"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        role=PIDRelation(
            "metadata.contributors.role",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-roles"),
        ),
        affiliations_item_1=PIDRelation(
            "metadata.contributors.affiliations",
            keys=["id", "title", {"key": "type.id", "target": "type"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        resourceType=PIDRelation(
            "metadata.resourceType",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("resource-types"),
        ),
        subjectCategories_item=PIDRelation(
            "metadata.subjectCategories",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("subject-categories"),
        ),
        languages_item=PIDRelation(
            "metadata.languages",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("languages"),
        ),
        rights_item=PIDRelation(
            "metadata.rights",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("licenses"),
        ),
        accessRights=PIDRelation(
            "metadata.accessRights",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("access-rights"),
        ),
        affiliations_item_2=PIDRelation(
            "metadata.relatedItems.itemCreators.affiliations",
            keys=["id", "title", {"key": "type.id", "target": "type"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        role_1=PIDRelation(
            "metadata.relatedItems.itemContributors.role",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("contributor-roles"),
        ),
        affiliations_item_3=PIDRelation(
            "metadata.relatedItems.itemContributors.affiliations",
            keys=["id", "title", {"key": "type.id", "target": "type"}, "hierarchy"],
            pid_field=Vocabulary.pid.with_type_ctx("institutions"),
        ),
        itemRelationType=PIDRelation(
            "metadata.relatedItems.itemRelationType",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("item-relation-types"),
        ),
        itemResourceType=PIDRelation(
            "metadata.relatedItems.itemResourceType",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("resource-types"),
        ),
        funder=PIDRelation(
            "metadata.fundingReferences.funder",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("funders"),
        ),
        country=PIDRelation(
            "metadata.events.eventLocation.country",
            keys=["id", "title", {"key": "type.id", "target": "type"}],
            pid_field=Vocabulary.pid.with_type_ctx("countries"),
        ),
    )
