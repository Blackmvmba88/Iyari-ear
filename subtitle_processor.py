#!/usr/bin/env python3
"""
Subtitle Processor - Optimización y Validación de Subtítulos
Procesa, valida y optimiza subtítulos para VLC y otros reproductores.
"""
import re
import os
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@dataclass
class SubtitleEntry:
    """Representa una entrada de subtítulo"""
    index: int
    start_time: timedelta
    end_time: timedelta
    text: str
    
    def __post_init__(self):
        """Validar datos al crear la entrada"""
        if self.start_time >= self.end_time:
            raise ValueError(f"Tiempo de inicio debe ser menor que tiempo final: {self.start_time} >= {self.end_time}")
        if not self.text.strip():
            raise ValueError("El texto del subtítulo no puede estar vacío")
    
    @property
    def duration(self) -> timedelta:
        """Duración del subtítulo"""
        return self.end_time - self.start_time
    
    def to_srt(self) -> str:
        """Convierte a formato SRT"""
        start = self._timedelta_to_srt(self.start_time)
        end = self._timedelta_to_srt(self.end_time)
        return f"{self.index}\n{start} --> {end}\n{self.text}\n"
    
    def to_vtt(self) -> str:
        """Convierte a formato VTT (WebVTT)"""
        start = self._timedelta_to_vtt(self.start_time)
        end = self._timedelta_to_vtt(self.end_time)
        return f"{start} --> {end}\n{self.text}\n"
    
    @staticmethod
    def _timedelta_to_srt(td: timedelta) -> str:
        """Convierte timedelta a formato SRT (HH:MM:SS,mmm)"""
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        milliseconds = td.microseconds // 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"
    
    @staticmethod
    def _timedelta_to_vtt(td: timedelta) -> str:
        """Convierte timedelta a formato VTT (HH:MM:SS.mmm)"""
        total_seconds = int(td.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        milliseconds = td.microseconds // 1000
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


class SubtitleProcessor:
    """Procesador principal de subtítulos"""
    
    # Configuración de optimización
    MIN_DURATION_MS = 500  # Duración mínima de un subtítulo (ms)
    MAX_DURATION_MS = 7000  # Duración máxima de un subtítulo (ms)
    MIN_GAP_MS = 100  # Espacio mínimo entre subtítulos (ms)
    MAX_CHARS_PER_LINE = 42  # Máximo de caracteres por línea
    MAX_LINES = 2  # Máximo de líneas por subtítulo
    
    def __init__(self):
        self.subtitles: List[SubtitleEntry] = []
        self.original_format: Optional[str] = None
    
    def load_from_file(self, filepath: str) -> bool:
        """Carga subtítulos desde un archivo"""
        if not os.path.exists(filepath):
            logger.error(f"Archivo no encontrado: {filepath}")
            return False
        
        ext = os.path.splitext(filepath)[1].lower()
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if ext == '.srt':
                self.original_format = 'srt'
                return self._parse_srt(content)
            elif ext == '.vtt':
                self.original_format = 'vtt'
                return self._parse_vtt(content)
            elif ext in ['.ass', '.ssa']:
                self.original_format = 'ass'
                return self._parse_ass(content)
            else:
                logger.error(f"Formato no soportado: {ext}")
                return False
        except Exception as e:
            logger.error(f"Error al cargar archivo: {e}")
            return False
    
    def _parse_srt(self, content: str) -> bool:
        """Parser para formato SRT"""
        self.subtitles = []
        
        # Patrón para entradas SRT
        pattern = r'(\d+)\s+(\d{2}:\d{2}:\d{2},\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2},\d{3})\s+((?:.*\n?)+?)(?=\n\d+\s+\d{2}:\d{2}:\d{2}|\Z)'
        
        matches = re.finditer(pattern, content, re.MULTILINE)
        
        for match in matches:
            try:
                index = int(match.group(1))
                start_time = self._parse_srt_time(match.group(2))
                end_time = self._parse_srt_time(match.group(3))
                text = match.group(4).strip()
                
                entry = SubtitleEntry(index, start_time, end_time, text)
                self.subtitles.append(entry)
            except ValueError as e:
                logger.warning(f"Entrada inválida ignorada: {e}")
                continue
        
        logger.info(f"Parseados {len(self.subtitles)} subtítulos SRT")
        return len(self.subtitles) > 0
    
    def _parse_vtt(self, content: str) -> bool:
        """Parser para formato WebVTT"""
        self.subtitles = []
        
        # Remover header WebVTT si existe
        content = re.sub(r'^WEBVTT.*\n\n', '', content, flags=re.MULTILINE)
        
        # Patrón para entradas VTT
        pattern = r'(\d{2}:\d{2}:\d{2}\.\d{3})\s+-->\s+(\d{2}:\d{2}:\d{2}\.\d{3})\s+((?:.*\n?)+?)(?=\n\d{2}:\d{2}:\d{2}|\Z)'
        
        matches = re.finditer(pattern, content, re.MULTILINE)
        
        index = 1
        for match in matches:
            try:
                start_time = self._parse_vtt_time(match.group(1))
                end_time = self._parse_vtt_time(match.group(2))
                text = match.group(3).strip()
                
                entry = SubtitleEntry(index, start_time, end_time, text)
                self.subtitles.append(entry)
                index += 1
            except ValueError as e:
                logger.warning(f"Entrada inválida ignorada: {e}")
                continue
        
        logger.info(f"Parseados {len(self.subtitles)} subtítulos VTT")
        return len(self.subtitles) > 0
    
    def _parse_ass(self, content: str) -> bool:
        """Parser para formato ASS/SSA (simplificado)"""
        self.subtitles = []
        
        # Buscar sección de eventos
        events_section = re.search(r'\[Events\](.*?)(?=\n\[|\Z)', content, re.DOTALL)
        if not events_section:
            logger.error("No se encontró sección [Events] en archivo ASS")
            return False
        
        # Patrón para diálogos
        pattern = r'Dialogue:\s*\d+,(\d+:\d{2}:\d{2}\.\d{2}),(\d+:\d{2}:\d{2}\.\d{2}),.*?,.*?,\d+,\d+,\d+,.*?,(.+?)$'
        
        matches = re.finditer(pattern, events_section.group(1), re.MULTILINE)
        
        index = 1
        for match in matches:
            try:
                start_time = self._parse_ass_time(match.group(1))
                end_time = self._parse_ass_time(match.group(2))
                text = self._clean_ass_text(match.group(3))
                
                entry = SubtitleEntry(index, start_time, end_time, text)
                self.subtitles.append(entry)
                index += 1
            except ValueError as e:
                logger.warning(f"Entrada inválida ignorada: {e}")
                continue
        
        logger.info(f"Parseados {len(self.subtitles)} subtítulos ASS")
        return len(self.subtitles) > 0
    
    @staticmethod
    def _parse_srt_time(time_str: str) -> timedelta:
        """Parsea tiempo en formato SRT (HH:MM:SS,mmm)"""
        match = re.match(r'(\d{2}):(\d{2}):(\d{2}),(\d{3})', time_str)
        if not match:
            raise ValueError(f"Formato de tiempo SRT inválido: {time_str}")
        
        hours, minutes, seconds, milliseconds = map(int, match.groups())
        return timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)
    
    @staticmethod
    def _parse_vtt_time(time_str: str) -> timedelta:
        """Parsea tiempo en formato VTT (HH:MM:SS.mmm)"""
        match = re.match(r'(\d{2}):(\d{2}):(\d{2})\.(\d{3})', time_str)
        if not match:
            raise ValueError(f"Formato de tiempo VTT inválido: {time_str}")
        
        hours, minutes, seconds, milliseconds = map(int, match.groups())
        return timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)
    
    @staticmethod
    def _parse_ass_time(time_str: str) -> timedelta:
        """Parsea tiempo en formato ASS (H:MM:SS.cc)"""
        match = re.match(r'(\d+):(\d{2}):(\d{2})\.(\d{2})', time_str)
        if not match:
            raise ValueError(f"Formato de tiempo ASS inválido: {time_str}")
        
        hours, minutes, seconds, centiseconds = map(int, match.groups())
        return timedelta(hours=hours, minutes=minutes, seconds=seconds, milliseconds=centiseconds*10)
    
    @staticmethod
    def _clean_ass_text(text: str) -> str:
        """Limpia etiquetas de formato ASS del texto"""
        # Remover etiquetas de estilo
        text = re.sub(r'\{[^}]+\}', '', text)
        # Remover saltos de línea codificados
        text = text.replace('\\N', '\n')
        text = text.replace('\\n', '\n')
        return text.strip()
    
    def validate(self) -> List[Dict[str, any]]:
        """Valida los subtítulos y retorna lista de problemas"""
        issues = []
        
        for i, entry in enumerate(self.subtitles):
            # Verificar duración mínima
            duration_ms = entry.duration.total_seconds() * 1000
            if duration_ms < self.MIN_DURATION_MS:
                issues.append({
                    'index': entry.index,
                    'type': 'duration_too_short',
                    'message': f'Subtítulo #{entry.index}: Duración muy corta ({duration_ms:.0f}ms)',
                    'severity': 'warning'
                })
            
            # Verificar duración máxima
            if duration_ms > self.MAX_DURATION_MS:
                issues.append({
                    'index': entry.index,
                    'type': 'duration_too_long',
                    'message': f'Subtítulo #{entry.index}: Duración muy larga ({duration_ms:.0f}ms)',
                    'severity': 'warning'
                })
            
            # Verificar número de líneas
            lines = entry.text.split('\n')
            if len(lines) > self.MAX_LINES:
                issues.append({
                    'index': entry.index,
                    'type': 'too_many_lines',
                    'message': f'Subtítulo #{entry.index}: Demasiadas líneas ({len(lines)})',
                    'severity': 'warning'
                })
            
            # Verificar longitud de líneas
            for line_num, line in enumerate(lines, 1):
                if len(line) > self.MAX_CHARS_PER_LINE:
                    issues.append({
                        'index': entry.index,
                        'type': 'line_too_long',
                        'message': f'Subtítulo #{entry.index}, línea {line_num}: Muy larga ({len(line)} chars)',
                        'severity': 'info'
                    })
            
            # Verificar superposición con siguiente subtítulo
            if i < len(self.subtitles) - 1:
                next_entry = self.subtitles[i + 1]
                if entry.end_time > next_entry.start_time:
                    issues.append({
                        'index': entry.index,
                        'type': 'overlap',
                        'message': f'Subtítulo #{entry.index} se superpone con #{next_entry.index}',
                        'severity': 'error'
                    })
                
                # Verificar espacio mínimo
                gap_ms = (next_entry.start_time - entry.end_time).total_seconds() * 1000
                if gap_ms < self.MIN_GAP_MS:
                    issues.append({
                        'index': entry.index,
                        'type': 'gap_too_small',
                        'message': f'Espacio muy pequeño entre #{entry.index} y #{next_entry.index} ({gap_ms:.0f}ms)',
                        'severity': 'info'
                    })
        
        logger.info(f"Validación completada: {len(issues)} problemas encontrados")
        return issues
    
    def optimize(self, fix_overlaps: bool = True, fix_durations: bool = True, 
                 split_long_lines: bool = True) -> int:
        """Optimiza los subtítulos aplicando correcciones automáticas"""
        changes = 0
        
        if fix_overlaps:
            changes += self._fix_overlaps()
        
        if fix_durations:
            changes += self._fix_durations()
        
        if split_long_lines:
            changes += self._split_long_lines()
        
        logger.info(f"Optimización completada: {changes} cambios realizados")
        return changes
    
    def _fix_overlaps(self) -> int:
        """Corrige superposiciones entre subtítulos"""
        changes = 0
        
        for i in range(len(self.subtitles) - 1):
            current = self.subtitles[i]
            next_entry = self.subtitles[i + 1]
            
            if current.end_time > next_entry.start_time:
                # Ajustar el final del subtítulo actual
                gap = timedelta(milliseconds=self.MIN_GAP_MS)
                current.end_time = next_entry.start_time - gap
                changes += 1
                logger.debug(f"Corregida superposición en subtítulo #{current.index}")
        
        return changes
    
    def _fix_durations(self) -> int:
        """Corrige duraciones anormales"""
        changes = 0
        
        for entry in self.subtitles:
            duration_ms = entry.duration.total_seconds() * 1000
            
            # Duración muy corta
            if duration_ms < self.MIN_DURATION_MS:
                additional_ms = self.MIN_DURATION_MS - duration_ms
                entry.end_time += timedelta(milliseconds=additional_ms)
                changes += 1
                logger.debug(f"Extendida duración del subtítulo #{entry.index}")
            
            # Duración muy larga
            elif duration_ms > self.MAX_DURATION_MS:
                entry.end_time = entry.start_time + timedelta(milliseconds=self.MAX_DURATION_MS)
                changes += 1
                logger.debug(f"Reducida duración del subtítulo #{entry.index}")
        
        return changes
    
    def _split_long_lines(self) -> int:
        """Divide líneas largas en múltiples líneas"""
        changes = 0
        
        for entry in self.subtitles:
            lines = entry.text.split('\n')
            new_lines = []
            
            for line in lines:
                if len(line) > self.MAX_CHARS_PER_LINE:
                    # Dividir en palabras
                    words = line.split()
                    current_line = []
                    
                    for word in words:
                        test_line = ' '.join(current_line + [word])
                        if len(test_line) <= self.MAX_CHARS_PER_LINE:
                            current_line.append(word)
                        else:
                            if current_line:
                                new_lines.append(' '.join(current_line))
                            current_line = [word]
                    
                    if current_line:
                        new_lines.append(' '.join(current_line))
                    
                    changes += 1
                else:
                    new_lines.append(line)
            
            # Limitar a MAX_LINES
            if len(new_lines) > self.MAX_LINES:
                new_lines = new_lines[:self.MAX_LINES]
            
            entry.text = '\n'.join(new_lines)
        
        return changes
    
    def save_to_file(self, filepath: str, format: Optional[str] = None) -> bool:
        """Guarda los subtítulos en un archivo"""
        if not self.subtitles:
            logger.error("No hay subtítulos para guardar")
            return False
        
        # Determinar formato
        if format is None:
            format = self.original_format or 'srt'
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                if format == 'srt':
                    for entry in self.subtitles:
                        f.write(entry.to_srt())
                        f.write('\n')
                elif format == 'vtt':
                    f.write('WEBVTT\n\n')
                    for entry in self.subtitles:
                        f.write(entry.to_vtt())
                        f.write('\n')
                else:
                    logger.error(f"Formato de salida no soportado: {format}")
                    return False
            
            logger.info(f"Subtítulos guardados en {filepath} (formato: {format})")
            return True
        except Exception as e:
            logger.error(f"Error al guardar archivo: {e}")
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas de los subtítulos"""
        if not self.subtitles:
            return {
                'total': 0,
                'total_duration': 0,
                'avg_duration': 0,
                'min_duration': 0,
                'max_duration': 0
            }
        
        durations = [s.duration.total_seconds() * 1000 for s in self.subtitles]
        
        return {
            'total': len(self.subtitles),
            'total_duration': sum(durations) / 1000,  # en segundos
            'avg_duration': sum(durations) / len(durations),  # en ms
            'min_duration': min(durations),  # en ms
            'max_duration': max(durations),  # en ms
            'start_time': str(self.subtitles[0].start_time) if self.subtitles else None,
            'end_time': str(self.subtitles[-1].end_time) if self.subtitles else None
        }


def process_subtitle_file(input_path: str, output_path: Optional[str] = None,
                          validate: bool = True, optimize: bool = True,
                          output_format: Optional[str] = None) -> Tuple[bool, Dict]:
    """
    Función de conveniencia para procesar un archivo de subtítulos
    
    Args:
        input_path: Ruta al archivo de entrada
        output_path: Ruta al archivo de salida (opcional)
        validate: Si se debe validar
        optimize: Si se debe optimizar
        output_format: Formato de salida (srt, vtt, etc.)
    
    Returns:
        Tuple de (éxito, resultados)
    """
    processor = SubtitleProcessor()
    results = {
        'loaded': False,
        'validation_issues': [],
        'optimization_changes': 0,
        'saved': False,
        'stats': {}
    }
    
    # Cargar archivo
    if not processor.load_from_file(input_path):
        return False, results
    
    results['loaded'] = True
    results['stats'] = processor.get_stats()
    
    # Validar
    if validate:
        results['validation_issues'] = processor.validate()
    
    # Optimizar
    if optimize:
        results['optimization_changes'] = processor.optimize()
        # Actualizar estadísticas después de optimización
        results['stats'] = processor.get_stats()
    
    # Guardar
    if output_path:
        results['saved'] = processor.save_to_file(output_path, output_format)
    
    return True, results


if __name__ == '__main__':
    # Configurar logging para modo standalone
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s: %(message)s'
    )
    
    # Ejemplo de uso
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python subtitle_processor.py <archivo_entrada> [archivo_salida]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    success, results = process_subtitle_file(
        input_file,
        output_file,
        validate=True,
        optimize=True
    )
    
    if success:
        print(f"\n✅ Procesamiento completado")
        print(f"   Subtítulos: {results['stats']['total']}")
        print(f"   Duración total: {results['stats']['total_duration']:.2f}s")
        print(f"   Problemas encontrados: {len(results['validation_issues'])}")
        print(f"   Cambios de optimización: {results['optimization_changes']}")
        if results['saved']:
            print(f"   Archivo guardado: {output_file}")
    else:
        print("\n❌ Error al procesar archivo")
        sys.exit(1)
