"""
Motor de Diagnóstico Real para Placas Electrónicas
Sistema de 3 capas: Localización -> Causa -> Consecuencia
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json


class DiagnosticStyle(Enum):
    """Estilos de diagnóstico disponibles"""
    TECHNICIAN = "técnico"  # Práctico, resolutivo
    ENGINEER = "ingeniero"  # Causal, metodológico
    FORENSIC = "forense"  # Detallista, profundo


class ComponentType(Enum):
    """Tipos de componentes electrónicos"""
    VOLTAGE_REGULATOR = "regulador_voltaje"
    CAPACITOR = "capacitor"
    RESISTOR = "resistor"
    IC = "circuito_integrado"
    CONNECTOR = "conector"
    INDUCTOR = "inductor"
    DIODE = "diodo"
    TRANSISTOR = "transistor"
    MCU = "microcontrolador"
    RF_MODULE = "modulo_rf"
    UNKNOWN = "desconocido"


class FaultCause(Enum):
    """Causas comunes de fallas"""
    NO_VOLTAGE = "sin_voltaje"
    OVERVOLTAGE = "sobrevoltaje"
    SHORT_CIRCUIT = "cortocircuito"
    OPEN_CIRCUIT = "circuito_abierto"
    OVERHEATING = "sobrecalentamiento"
    ESD_DAMAGE = "daño_esd"
    CORROSION = "corrosion"
    MECHANICAL_DAMAGE = "daño_mecanico"
    COMPONENT_FAILURE = "falla_componente"
    SIGNAL_LOSS = "perdida_señal"
    UNKNOWN = "desconocida"


class ImpactLevel(Enum):
    """Nivel de impacto de la falla"""
    CRITICAL = "crítico"  # Placa no arranca
    HIGH = "alto"  # Funcionalidad principal afectada
    MEDIUM = "medio"  # Funcionalidad secundaria afectada
    LOW = "bajo"  # Funcionalidad menor afectada


@dataclass
class Component:
    """Representa un componente detectado en la placa"""
    component_id: str
    component_type: ComponentType
    location: Tuple[int, int]  # (x, y) en la imagen
    confidence: float  # 0.0 a 1.0
    label: str = ""  # Etiqueta del componente (ej: "U1", "C15")
    value: str = ""  # Valor del componente (ej: "1117", "10uF")
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class VoltageRail:
    """Representa un rail de voltaje en la placa"""
    rail_id: str
    voltage: float  # Voltaje nominal
    name: str  # Ej: "3V3", "5V", "VBAT"
    source_component: Optional[str] = None  # ID del regulador/fuente
    connected_components: List[str] = field(default_factory=list)
    expected_current: Optional[float] = None  # Corriente esperada en mA


@dataclass
class FunctionalBlock:
    """Representa un bloque funcional de la placa"""
    block_id: str
    name: str  # Ej: "RF", "Power", "MCU", "USB"
    components: List[str] = field(default_factory=list)
    rails: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)  # Otros bloques necesarios


@dataclass
class DiagnosticLayer1:
    """Capa 1: Localización - Dónde está la falla"""
    component_id: Optional[str] = None
    component_type: Optional[ComponentType] = None
    location: Optional[Tuple[int, int]] = None
    functional_block: Optional[str] = None
    voltage_rail: Optional[str] = None
    confidence: float = 0.0


@dataclass
class DiagnosticLayer2:
    """Capa 2: Causa - Por qué existe la falla"""
    fault_cause: FaultCause = FaultCause.UNKNOWN
    evidence: List[str] = field(default_factory=list)
    reasoning: str = ""
    confidence: float = 0.0


@dataclass
class DiagnosticLayer3:
    """Capa 3: Consecuencia - Qué rompe funcionalmente"""
    functional_impact: str = ""
    impact_level: ImpactLevel = ImpactLevel.LOW
    affected_features: List[str] = field(default_factory=list)
    cascading_effects: List[str] = field(default_factory=list)


@dataclass
class DiagnosticHypothesis:
    """Hipótesis de diagnóstico completa (3 capas)"""
    hypothesis_id: str
    layer1: DiagnosticLayer1
    layer2: DiagnosticLayer2
    layer3: DiagnosticLayer3
    overall_confidence: float = 0.0
    next_steps: List[str] = field(default_factory=list)
    test_points: List[str] = field(default_factory=list)


@dataclass
class BoardImage:
    """Representa una imagen de la placa"""
    image_id: str
    image_path: str
    image_type: str  # "frontal", "backside", "closeup", "microscope", "rf_area", "power_area"
    timestamp: datetime = field(default_factory=datetime.now)
    components_detected: List[Component] = field(default_factory=list)
    annotations: List[str] = field(default_factory=list)


@dataclass
class DiagnosticSession:
    """Sesión completa de diagnóstico de una placa"""
    session_id: str
    board_model: str
    creation_time: datetime = field(default_factory=datetime.now)
    images: List[BoardImage] = field(default_factory=list)
    components: List[Component] = field(default_factory=list)
    rails: List[VoltageRail] = field(default_factory=list)
    functional_blocks: List[FunctionalBlock] = field(default_factory=list)
    hypotheses: List[DiagnosticHypothesis] = field(default_factory=list)
    measurements: Dict[str, Any] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)
    diagnostic_style: DiagnosticStyle = DiagnosticStyle.TECHNICIAN
    status: str = "iniciada"  # iniciada, en_progreso, completada


class DiagnosticEngine:
    """Motor principal de diagnóstico"""
    
    def __init__(self, style: DiagnosticStyle = DiagnosticStyle.TECHNICIAN):
        self.style = style
        self.sessions: Dict[str, DiagnosticSession] = {}
        
        # Base de conocimiento básica
        self.component_library = self._init_component_library()
        self.common_rails = self._init_common_rails()
        self.typical_blocks = self._init_typical_blocks()
    
    def _init_component_library(self) -> Dict[str, Dict[str, Any]]:
        """Inicializa biblioteca de componentes comunes"""
        return {
            "AMS1117": {
                "type": ComponentType.VOLTAGE_REGULATOR,
                "typical_output": 3.3,
                "failure_modes": ["sin_salida", "salida_baja", "sobrecalentamiento"],
                "impact": "Si falla, 3V3 no llega, RF queda muerto, placa no arranca"
            },
            "1117": {
                "type": ComponentType.VOLTAGE_REGULATOR,
                "typical_output": 3.3,
                "failure_modes": ["sin_salida", "salida_baja"],
                "impact": "Rail de 3.3V ausente o bajo"
            },
            "ESP32": {
                "type": ComponentType.MCU,
                "voltage_rails": ["3V3", "1V8"],
                "failure_modes": ["no_boot", "reset_continuo", "sin_programa"],
                "impact": "Procesador no funciona, sin WiFi/BT"
            }
        }
    
    def _init_common_rails(self) -> List[str]:
        """Rails de voltaje comunes"""
        return ["5V", "3V3", "1V8", "VBAT", "USB_5V", "VDD_RF"]
    
    def _init_typical_blocks(self) -> List[str]:
        """Bloques funcionales típicos"""
        return ["Power", "MCU", "RF", "USB", "Sensors", "Memory", "IO"]
    
    def create_session(self, board_model: str, session_id: Optional[str] = None) -> str:
        """Crea una nueva sesión de diagnóstico"""
        if session_id is None:
            session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        session = DiagnosticSession(
            session_id=session_id,
            board_model=board_model,
            diagnostic_style=self.style
        )
        
        self.sessions[session_id] = session
        return session_id
    
    def add_image(self, session_id: str, image_path: str, image_type: str = "frontal") -> str:
        """Añade una imagen a la sesión"""
        if session_id not in self.sessions:
            raise ValueError(f"Sesión {session_id} no encontrada")
        
        session = self.sessions[session_id]
        image_id = f"img_{len(session.images) + 1}"
        
        board_image = BoardImage(
            image_id=image_id,
            image_path=image_path,
            image_type=image_type
        )
        
        session.images.append(board_image)
        return image_id
    
    def analyze_image(self, session_id: str, image_id: str) -> Dict[str, Any]:
        """
        Analiza una imagen y detecta componentes
        En producción, aquí iría un modelo de ML/CV
        """
        if session_id not in self.sessions:
            raise ValueError(f"Sesión {session_id} no encontrada")
        
        session = self.sessions[session_id]
        
        # Placeholder: En producción usaría YOLO/CV para detectar componentes
        status_updates = [
            "✔ Identificando rails...",
            "✔ Detectando componentes de potencia...",
            "✔ Analizando topología...",
            "✔ Buscando reguladores..."
        ]
        
        return {
            "status": "analyzing",
            "image_id": image_id,
            "updates": status_updates
        }
    
    def generate_hypothesis_layer1(
        self, 
        session_id: str,
        component_id: Optional[str] = None,
        rail: Optional[str] = None
    ) -> DiagnosticLayer1:
        """Genera hipótesis de Capa 1: Localización"""
        
        # Ejemplo simple de localización
        return DiagnosticLayer1(
            component_id=component_id,
            voltage_rail=rail,
            confidence=0.8
        )
    
    def generate_hypothesis_layer2(
        self,
        layer1: DiagnosticLayer1,
        component_info: Optional[Dict[str, Any]] = None
    ) -> DiagnosticLayer2:
        """Genera hipótesis de Capa 2: Causa raíz"""
        
        reasoning = ""
        fault_cause = FaultCause.UNKNOWN
        evidence = []
        
        # Lógica de razonamiento según estilo
        if self.style == DiagnosticStyle.TECHNICIAN:
            reasoning = "Análisis práctico basado en síntomas comunes"
            if layer1.voltage_rail == "3V3":
                fault_cause = FaultCause.NO_VOLTAGE
                evidence.append("Rail 3V3 identificado")
                evidence.append("Regulador probable: AMS1117 o similar")
                reasoning = "Si 3V3 está ausente, probable falla en regulador de voltaje"
        
        elif self.style == DiagnosticStyle.ENGINEER:
            reasoning = "Análisis causal sistemático desde topología"
            
        elif self.style == DiagnosticStyle.FORENSIC:
            reasoning = "Análisis detallado de todas las rutas de señal"
        
        return DiagnosticLayer2(
            fault_cause=fault_cause,
            evidence=evidence,
            reasoning=reasoning,
            confidence=0.75
        )
    
    def generate_hypothesis_layer3(
        self,
        layer1: DiagnosticLayer1,
        layer2: DiagnosticLayer2
    ) -> DiagnosticLayer3:
        """Genera hipótesis de Capa 3: Impacto funcional"""
        
        functional_impact = ""
        impact_level = ImpactLevel.LOW
        affected_features = []
        
        # Determinar impacto basado en rail/componente
        if layer1.voltage_rail == "3V3":
            functional_impact = "Radio no enciende, placa no arranca"
            impact_level = ImpactLevel.CRITICAL
            affected_features = ["WiFi", "Bluetooth", "RF", "MCU"]
        
        elif layer1.voltage_rail == "5V":
            functional_impact = "Sin alimentación USB, reguladores no funcionan"
            impact_level = ImpactLevel.CRITICAL
            affected_features = ["USB", "Alimentación", "Carga"]
        
        return DiagnosticLayer3(
            functional_impact=functional_impact,
            impact_level=impact_level,
            affected_features=affected_features
        )
    
    def generate_full_hypothesis(
        self,
        session_id: str,
        component_id: Optional[str] = None,
        rail: Optional[str] = None
    ) -> DiagnosticHypothesis:
        """Genera hipótesis completa de 3 capas"""
        
        layer1 = self.generate_hypothesis_layer1(session_id, component_id, rail)
        layer2 = self.generate_hypothesis_layer2(layer1)
        layer3 = self.generate_hypothesis_layer3(layer1, layer2)
        
        # Calcular confianza general
        overall_confidence = (
            layer1.confidence * 0.4 +
            layer2.confidence * 0.3 +
            0.3  # Base para layer3
        )
        
        # Generar próximos pasos según el estilo
        next_steps = self._generate_next_steps(layer1, layer2, layer3)
        test_points = self._generate_test_points(layer1, layer2)
        
        hypothesis_id = f"hyp_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
        
        return DiagnosticHypothesis(
            hypothesis_id=hypothesis_id,
            layer1=layer1,
            layer2=layer2,
            layer3=layer3,
            overall_confidence=overall_confidence,
            next_steps=next_steps,
            test_points=test_points
        )
    
    def _generate_next_steps(
        self,
        layer1: DiagnosticLayer1,
        layer2: DiagnosticLayer2,
        layer3: DiagnosticLayer3
    ) -> List[str]:
        """Genera próximos pasos de diagnóstico"""
        
        steps = []
        
        if layer1.voltage_rail:
            steps.append(f"Medir voltaje en rail {layer1.voltage_rail}")
        
        if layer2.fault_cause == FaultCause.NO_VOLTAGE:
            steps.append("Verificar continuidad desde fuente")
            steps.append("Revisar regulador de voltaje")
        
        if layer3.impact_level in [ImpactLevel.CRITICAL, ImpactLevel.HIGH]:
            steps.append("Prioridad alta: Resolver antes de continuar")
        
        return steps
    
    def _generate_test_points(
        self,
        layer1: DiagnosticLayer1,
        layer2: DiagnosticLayer2
    ) -> List[str]:
        """Genera puntos de prueba sugeridos"""
        
        test_points = []
        
        if layer1.voltage_rail == "3V3":
            test_points.extend(["TP3", "TP_3V3", "Salida del regulador U1"])
        
        if layer1.voltage_rail == "5V":
            test_points.extend(["TP1", "TP_5V", "Pin VBUS USB"])
        
        return test_points
    
    def get_diagnostic_summary(self, session_id: str) -> Dict[str, Any]:
        """Obtiene resumen del diagnóstico"""
        
        if session_id not in self.sessions:
            raise ValueError(f"Sesión {session_id} no encontrada")
        
        session = self.sessions[session_id]
        
        return {
            "session_id": session.session_id,
            "board_model": session.board_model,
            "images_count": len(session.images),
            "hypotheses_count": len(session.hypotheses),
            "status": session.status,
            "style": session.diagnostic_style.value,
            "creation_time": session.creation_time.isoformat()
        }
    
    def format_diagnostic_report(self, session_id: str) -> str:
        """Formatea un reporte de diagnóstico legible"""
        
        if session_id not in self.sessions:
            raise ValueError(f"Sesión {session_id} no encontrada")
        
        session = self.sessions[session_id]
        
        report = f"""
═══════════════════════════════════════════════════════════
   REPORTE DE DIAGNÓSTICO ELECTRÓNICO
═══════════════════════════════════════════════════════════

Sesión: {session.session_id}
Placa: {session.board_model}
Fecha: {session.creation_time.strftime('%Y-%m-%d %H:%M:%S')}
Estilo: {session.diagnostic_style.value.upper()}

───────────────────────────────────────────────────────────
IMÁGENES ANALIZADAS ({len(session.images)})
───────────────────────────────────────────────────────────
"""
        
        for img in session.images:
            report += f"  • {img.image_type}: {img.image_id}\n"
        
        report += f"""
───────────────────────────────────────────────────────────
HIPÓTESIS DE DIAGNÓSTICO ({len(session.hypotheses)})
───────────────────────────────────────────────────────────
"""
        
        for i, hyp in enumerate(session.hypotheses, 1):
            report += f"""
Hipótesis #{i} (Confianza: {hyp.overall_confidence*100:.1f}%)

  📍 CAPA 1 - LOCALIZACIÓN:
     • Rail: {hyp.layer1.voltage_rail or 'N/A'}
     • Componente: {hyp.layer1.component_id or 'N/A'}
     • Bloque: {hyp.layer1.functional_block or 'N/A'}

  🔍 CAPA 2 - CAUSA:
     • Causa: {hyp.layer2.fault_cause.value}
     • Razonamiento: {hyp.layer2.reasoning}
     • Evidencia: {', '.join(hyp.layer2.evidence) if hyp.layer2.evidence else 'Ninguna'}

  ⚡ CAPA 3 - CONSECUENCIA:
     • Impacto: {hyp.layer3.impact_level.value.upper()}
     • Efecto: {hyp.layer3.functional_impact}
     • Afecta: {', '.join(hyp.layer3.affected_features) if hyp.layer3.affected_features else 'N/A'}

  🔧 PRÓXIMOS PASOS:
"""
            for step in hyp.next_steps:
                report += f"     • {step}\n"
            
            if hyp.test_points:
                report += f"  📊 PUNTOS DE PRUEBA: {', '.join(hyp.test_points)}\n"
        
        report += "\n═══════════════════════════════════════════════════════════\n"
        
        return report
    
    def export_session(self, session_id: str) -> Dict[str, Any]:
        """Exporta sesión a formato JSON serializable"""
        
        if session_id not in self.sessions:
            raise ValueError(f"Sesión {session_id} no encontrada")
        
        session = self.sessions[session_id]
        
        # Convertir dataclasses a dict
        return {
            "session_id": session.session_id,
            "board_model": session.board_model,
            "creation_time": session.creation_time.isoformat(),
            "images": [
                {
                    "image_id": img.image_id,
                    "path": img.image_path,
                    "type": img.image_type,
                    "timestamp": img.timestamp.isoformat()
                }
                for img in session.images
            ],
            "hypotheses": [
                {
                    "hypothesis_id": hyp.hypothesis_id,
                    "confidence": hyp.overall_confidence,
                    "layer1": {
                        "rail": hyp.layer1.voltage_rail,
                        "component": hyp.layer1.component_id
                    },
                    "layer2": {
                        "cause": hyp.layer2.fault_cause.value,
                        "reasoning": hyp.layer2.reasoning
                    },
                    "layer3": {
                        "impact": hyp.layer3.functional_impact,
                        "level": hyp.layer3.impact_level.value
                    },
                    "next_steps": hyp.next_steps,
                    "test_points": hyp.test_points
                }
                for hyp in session.hypotheses
            ],
            "status": session.status,
            "style": session.diagnostic_style.value
        }
