import pytest
from bson import ObjectId
from planner.routes.base_models import PyObjectId
from pydantic import ConfigDict, TypeAdapter


@pytest.mark.parametrize("obj", ["64b7992ba8f08069073f1055", ObjectId("64b7992ba8f08069073f1055")])
def test_pyobjectid_validation(obj):
    ta = TypeAdapter(PyObjectId, config=ConfigDict(arbitrary_types_allowed=True))
    ta.validate_python(obj)


@pytest.mark.parametrize("obj", ["64b7992ba8f08069073f1055", ObjectId("64b7992ba8f08069073f1055")])
def test_pyobjectid_serialization(obj):
    ta = TypeAdapter(PyObjectId, config=ConfigDict(arbitrary_types_allowed=True))
    ta.dump_json(obj)
