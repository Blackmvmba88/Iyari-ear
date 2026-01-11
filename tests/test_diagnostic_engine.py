"""
Unit tests for the electronic diagnostic engine
"""

import pytest
from diagnostic_engine import (
    DiagnosticEngine,
    DiagnosticStyle,
    ComponentType,
    FaultCause,
    ImpactLevel
)


class TestDiagnosticEngine:
    """Tests para DiagnosticEngine"""
    
    def test_create_engine(self):
        """Test crear motor de diagnóstico"""
        engine = DiagnosticEngine(style=DiagnosticStyle.TECHNICIAN)
        assert engine is not None
        assert engine.style == DiagnosticStyle.TECHNICIAN
    
    def test_create_session(self):
        """Test crear sesión de diagnóstico"""
        engine = DiagnosticEngine()
        session_id = engine.create_session("ESP32-DevKit")
        
        assert session_id in engine.sessions
        assert engine.sessions[session_id].board_model == "ESP32-DevKit"
        assert engine.sessions[session_id].status == "iniciada"
    
    def test_add_image(self):
        """Test agregar imagen a sesión"""
        engine = DiagnosticEngine()
        session_id = engine.create_session("ESP32")
        
        image_id = engine.add_image(session_id, "/tmp/test.jpg", "frontal")
        
        assert image_id == "img_1"
        session = engine.sessions[session_id]
        assert len(session.images) == 1
        assert session.images[0].image_type == "frontal"
    
    def test_generate_hypothesis_layer1(self):
        """Test generar hipótesis capa 1"""
        engine = DiagnosticEngine()
        session_id = engine.create_session("ESP32")
        
        layer1 = engine.generate_hypothesis_layer1(
            session_id=session_id,
            component_id="U1",
            rail="3V3"
        )
        
        assert layer1 is not None
        assert layer1.component_id == "U1"
        assert layer1.voltage_rail == "3V3"
        assert layer1.confidence > 0
    
    def test_generate_hypothesis_layer2(self):
        """Test generar hipótesis capa 2"""
        engine = DiagnosticEngine(style=DiagnosticStyle.TECHNICIAN)
        session_id = engine.create_session("ESP32")
        
        layer1 = engine.generate_hypothesis_layer1(session_id, rail="3V3")
        layer2 = engine.generate_hypothesis_layer2(layer1)
        
        assert layer2 is not None
        assert layer2.fault_cause == FaultCause.NO_VOLTAGE
        assert len(layer2.evidence) > 0
        assert layer2.reasoning != ""
    
    def test_generate_hypothesis_layer3(self):
        """Test generar hipótesis capa 3"""
        engine = DiagnosticEngine()
        session_id = engine.create_session("ESP32")
        
        layer1 = engine.generate_hypothesis_layer1(session_id, rail="3V3")
        layer2 = engine.generate_hypothesis_layer2(layer1)
        layer3 = engine.generate_hypothesis_layer3(layer1, layer2)
        
        assert layer3 is not None
        assert layer3.impact_level == ImpactLevel.CRITICAL
        assert layer3.functional_impact != ""
        assert len(layer3.affected_features) > 0
    
    def test_generate_full_hypothesis(self):
        """Test generar hipótesis completa de 3 capas"""
        engine = DiagnosticEngine()
        session_id = engine.create_session("ESP32")
        
        hypothesis = engine.generate_full_hypothesis(
            session_id=session_id,
            rail="3V3"
        )
        
        assert hypothesis is not None
        assert hypothesis.layer1.voltage_rail == "3V3"
        assert hypothesis.layer2.fault_cause == FaultCause.NO_VOLTAGE
        assert hypothesis.layer3.impact_level == ImpactLevel.CRITICAL
        assert hypothesis.overall_confidence > 0
        assert len(hypothesis.next_steps) > 0
        assert len(hypothesis.test_points) > 0
    
    def test_diagnostic_styles(self):
        """Test diferentes estilos de diagnóstico"""
        # Técnico
        engine_tech = DiagnosticEngine(style=DiagnosticStyle.TECHNICIAN)
        session_id = engine_tech.create_session("ESP32")
        hyp_tech = engine_tech.generate_full_hypothesis(session_id, rail="3V3")
        assert "práctico" in hyp_tech.layer2.reasoning.lower() or "análisis" in hyp_tech.layer2.reasoning.lower()
        
        # Ingeniero
        engine_eng = DiagnosticEngine(style=DiagnosticStyle.ENGINEER)
        session_id2 = engine_eng.create_session("ESP32")
        hyp_eng = engine_eng.generate_full_hypothesis(session_id2, rail="3V3")
        assert hyp_eng.layer2.reasoning != ""
        
        # Forense
        engine_for = DiagnosticEngine(style=DiagnosticStyle.FORENSIC)
        session_id3 = engine_for.create_session("ESP32")
        hyp_for = engine_for.generate_full_hypothesis(session_id3, rail="3V3")
        assert hyp_for.layer2.reasoning != ""
    
    def test_format_diagnostic_report(self):
        """Test formatear reporte de diagnóstico"""
        engine = DiagnosticEngine()
        session_id = engine.create_session("ESP32-DevKit")
        
        # Agregar una hipótesis
        hyp = engine.generate_full_hypothesis(session_id, rail="3V3")
        engine.sessions[session_id].hypotheses.append(hyp)
        
        report = engine.format_diagnostic_report(session_id)
        
        assert "REPORTE DE DIAGNÓSTICO ELECTRÓNICO" in report
        assert "ESP32-DevKit" in report
        assert "3V3" in report
        assert "CAPA 1" in report
        assert "CAPA 2" in report
        assert "CAPA 3" in report
    
    def test_export_session(self):
        """Test exportar sesión a JSON"""
        engine = DiagnosticEngine()
        session_id = engine.create_session("ESP32")
        
        # Agregar imagen e hipótesis
        engine.add_image(session_id, "/tmp/test.jpg", "frontal")
        hyp = engine.generate_full_hypothesis(session_id, rail="3V3")
        engine.sessions[session_id].hypotheses.append(hyp)
        
        export = engine.export_session(session_id)
        
        assert export["session_id"] == session_id
        assert export["board_model"] == "ESP32"
        assert len(export["images"]) == 1
        assert len(export["hypotheses"]) == 1
        assert export["hypotheses"][0]["layer1"]["rail"] == "3V3"
    
    def test_get_diagnostic_summary(self):
        """Test obtener resumen de diagnóstico"""
        engine = DiagnosticEngine()
        session_id = engine.create_session("ESP32")
        
        summary = engine.get_diagnostic_summary(session_id)
        
        assert summary["session_id"] == session_id
        assert summary["board_model"] == "ESP32"
        assert summary["images_count"] == 0
        assert summary["hypotheses_count"] == 0
        assert summary["status"] == "iniciada"
    
    def test_component_library(self):
        """Test biblioteca de componentes"""
        engine = DiagnosticEngine()
        
        assert "AMS1117" in engine.component_library
        assert engine.component_library["AMS1117"]["type"] == ComponentType.VOLTAGE_REGULATOR
        assert engine.component_library["AMS1117"]["typical_output"] == 3.3
    
    def test_multiple_sessions(self):
        """Test múltiples sesiones simultáneas"""
        engine = DiagnosticEngine()
        
        session1 = engine.create_session("ESP32")
        session2 = engine.create_session("iPhone 12")
        session3 = engine.create_session("DJI Phantom")
        
        assert len(engine.sessions) == 3
        assert engine.sessions[session1].board_model == "ESP32"
        assert engine.sessions[session2].board_model == "iPhone 12"
        assert engine.sessions[session3].board_model == "DJI Phantom"
    
    def test_next_steps_generation(self):
        """Test generación de próximos pasos"""
        engine = DiagnosticEngine()
        session_id = engine.create_session("ESP32")
        
        hyp = engine.generate_full_hypothesis(session_id, rail="3V3")
        
        assert len(hyp.next_steps) > 0
        assert any("medir" in step.lower() for step in hyp.next_steps)
    
    def test_test_points_generation(self):
        """Test generación de puntos de prueba"""
        engine = DiagnosticEngine()
        session_id = engine.create_session("ESP32")
        
        hyp = engine.generate_full_hypothesis(session_id, rail="3V3")
        
        assert len(hyp.test_points) > 0
        assert any("TP" in point or "3V3" in point for point in hyp.test_points)


class TestDiagnosticModels:
    """Tests para modelos de datos"""
    
    def test_component_creation(self):
        """Test crear componente"""
        from diagnostic_engine import Component
        
        component = Component(
            component_id="U1",
            component_type=ComponentType.VOLTAGE_REGULATOR,
            location=(100, 200),
            confidence=0.95,
            label="AMS1117",
            value="3.3V"
        )
        
        assert component.component_id == "U1"
        assert component.component_type == ComponentType.VOLTAGE_REGULATOR
        assert component.location == (100, 200)
        assert component.confidence == 0.95
    
    def test_voltage_rail_creation(self):
        """Test crear rail de voltaje"""
        from diagnostic_engine import VoltageRail
        
        rail = VoltageRail(
            rail_id="rail_3v3",
            voltage=3.3,
            name="3V3",
            source_component="U1"
        )
        
        assert rail.rail_id == "rail_3v3"
        assert rail.voltage == 3.3
        assert rail.name == "3V3"
        assert rail.source_component == "U1"
    
    def test_functional_block_creation(self):
        """Test crear bloque funcional"""
        from diagnostic_engine import FunctionalBlock
        
        block = FunctionalBlock(
            block_id="power_block",
            name="Power Supply",
            components=["U1", "C1", "C2"],
            rails=["5V", "3V3"]
        )
        
        assert block.block_id == "power_block"
        assert block.name == "Power Supply"
        assert len(block.components) == 3
        assert len(block.rails) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
