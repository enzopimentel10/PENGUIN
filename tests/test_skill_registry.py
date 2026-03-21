import pytest
import os
from scripts.skills.skill_registry import registry, _get_safe_path

def test_initial_skills():
    skills = registry.list_skills()
    assert "create_file" in skills
    assert "read_file" in skills
    assert "write_file" in skills
    assert "list_directory" in skills

def test_get_skill():
    skill = registry.get_skill("read_file")
    assert callable(skill)
    
    skill_none = registry.get_skill("unknown_skill")
    assert skill_none is None

def test_safe_path_traversal():
    with pytest.raises(PermissionError):
        _get_safe_path("../../../etc/passwd")

def test_get_safe_path_creates_dir(tmp_path):
    import scripts.skills.skill_registry
    original_dir = scripts.skills.skill_registry.ARTIFACTS_DIR
    scripts.skills.skill_registry.ARTIFACTS_DIR = str(tmp_path / "artifacts")
    
    # Dir should not exist yet
    assert not os.path.exists(str(tmp_path / "artifacts"))
    
    path = _get_safe_path("test.txt")
    
    # Dir should exist now
    assert os.path.exists(str(tmp_path / "artifacts"))
    assert path.endswith("test.txt")
    
    # Cleanup
    scripts.skills.skill_registry.ARTIFACTS_DIR = original_dir
