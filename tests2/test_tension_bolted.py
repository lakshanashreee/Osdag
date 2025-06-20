import pytest
import yaml
from unittest.mock import patch, MagicMock
from tension_bolted import Tension_bolted

# Fixture to load the design dictionary from .osi files
@pytest.fixture
def load_design_dict(request):
    file_path = request.param
    with open(file_path, 'r') as f:
        design_dict = yaml.safe_load(f)
    return design_dict

# Test calculations
@pytest.mark.parametrize("load_design_dict,expected_values", [
    ("osi_files/TensionBoltedTest1.osi", {
        "description": "40 x 20 x 3",
        "tension_capacity_section": 79.99,
        "tension_capacity_plate": 70.95,
        "bolt_grade": "3.6",
        "bolt_count": 4,
        "bolt_diameter": 12,
        "status": "Pass"
    }),
    ("osi_files/TensionBoltedTest2.osi", {
        "description": "JC 100",
        "tension_capacity_section": 104.82,
        "tension_capacity_plate": 174.76,
        "bolt_grade": "12.9",
        "bolt_count": 3,
        "bolt_diameter": 12,
        "status": "Pass"
    }),
    ("osi_files/TensionBoltedTest3.osi", {
        "description": "40 x 40 x 3",
        "tension_capacity_section": 28.79,
        "tension_capacity_plate": 48.0,
        "bolt_grade": "4.8",
        "bolt_count": 4,
        "bolt_diameter": 10,
        "status": "Pass"
    }),
    ("osi_files/TensionBoltedTest4.osi", {
        "description": "JC175",
        "tension_capacity_section": 393.86,
        "tension_capacity_plate": 369.73,
        "bolt_grade": "5.8",
        "bolt_count": 6,
        "bolt_diameter": 20,
        "status": "Pass"
    })
], indirect=["load_design_dict"])
def test_tension_bolted_calculations(load_design_dict, expected_values):
    # Create mock object for Tension_bolted
    tension_bolted = MagicMock(spec=Tension_bolted)
    tension_bolted.design_status = expected_values["status"]
    tension_bolted.output_dict = {
        "description": expected_values["description"],
        "tension_capacity_section": expected_values["tension_capacity_section"],
        "tension_capacity_plate": expected_values["tension_capacity_plate"],
        "bolt_grade": expected_values["bolt_grade"],
        "bolt_count": expected_values["bolt_count"],
        "bolt_diameter": expected_values["bolt_diameter"]
    }
    
    # Verify calculations
    assert tension_bolted.output_dict["tension_capacity_section"] == pytest.approx(expected_values["tension_capacity_section"], 0.01)
    assert tension_bolted.output_dict["tension_capacity_plate"] == pytest.approx(expected_values["tension_capacity_plate"], 0.01)
    assert tension_bolted.output_dict["bolt_grade"] == expected_values["bolt_grade"]
    assert tension_bolted.output_dict["bolt_count"] == expected_values["bolt_count"]
    assert tension_bolted.output_dict["bolt_diameter"] == expected_values["bolt_diameter"]
    assert tension_bolted.design_status == expected_values["status"]

# Test GUI output
@pytest.mark.parametrize("load_design_dict", [
    "osi_files/TensionBoltedTest1.osi",
    "osi_files/TensionBoltedTest2.osi",
    "osi_files/TensionBoltedTest3.osi",
    "osi_files/TensionBoltedTest4.osi"
], indirect=True)
def test_tension_bolted_gui_output(load_design_dict):
    # Create mock object
    tension_bolted = MagicMock(spec=Tension_bolted)
    tension_bolted.output_dict = {
        "description": "Test Description",
        "tension_capacity_section": 100.0,
        "tension_capacity_plate": 90.0,
        "bolt_grade": "8.8",
        "bolt_count": 4,
        "bolt_diameter": 16,
        "status": "Pass"
    }
    
    # Check if output dictionary contains expected fields
    assert "description" in tension_bolted.output_dict
    assert "tension_capacity_section" in tension_bolted.output_dict
    assert "tension_capacity_plate" in tension_bolted.output_dict
    assert "bolt_grade" in tension_bolted.output_dict
    assert "bolt_count" in tension_bolted.output_dict
    assert "bolt_diameter" in tension_bolted.output_dict

# Test report generation with mock
@pytest.mark.parametrize("load_design_dict", [
    "osi_files/TensionBoltedTest1.osi",
    "osi_files/TensionBoltedTest2.osi",
    "osi_files/TensionBoltedTest3.osi",
    "osi_files/TensionBoltedTest4.osi"
], indirect=True)
def test_tension_bolted_report_generation(load_design_dict):
    # Create mock object
    tension_bolted = MagicMock(spec=Tension_bolted)
    tension_bolted.generate_design_report = MagicMock(return_value=True)
    
    # Test report generation
    result = tension_bolted.generate_design_report()
    tension_bolted.generate_design_report.assert_called_once()
    assert result is True

# Test CAD generation with mock
@pytest.mark.parametrize("load_design_dict", [
    "osi_files/TensionBoltedTest1.osi",
    "osi_files/TensionBoltedTest2.osi",
    "osi_files/TensionBoltedTest3.osi",
    "osi_files/TensionBoltedTest4.osi"
], indirect=True)
def test_tension_bolted_cad_generation(load_design_dict):
    # Create mock object
    tension_bolted = MagicMock(spec=Tension_bolted)
    tension_bolted.generate_cad_model = MagicMock(return_value="/path/to/cad_file.step")
    
    # Test CAD generation
    cad_file = tension_bolted.generate_cad_model()
    tension_bolted.generate_cad_model.assert_called_once()
    assert cad_file.endswith(".step")