# Iyari-ear Project Roadmap

## Introducción

Este documento describe la visión a futuro para el proyecto Iyari-ear. El objetivo es evolucionar la herramienta de un proyecto personal a una solución robusta y confiable para la comunidad, manteniendo siempre el espíritu de "creado con cariño para una amiga".

## Principios Guía

1.  **Accesibilidad Primero**: Cada nueva característica debe ser diseñada pensando en la facilidad de uso para personas con discapacidades auditivas.
2.  **Privacidad por Diseño**: No se almacenarán ni transmitirán conversaciones. La confianza del usuario es primordial.
3.  **Rendimiento en el Mundo Real**: La aplicación debe ser rápida y precisa en condiciones cotidianas (ej. cafeterías, reuniones familiares).
4.  **Comunidad y Colaboración**: Fomentar un entorno donde los usuarios puedan dar feedback y los desarrolladores puedan contribuir fácilmente.

## Roadmap de Épicas

### Épica 1: Robustecer y Validar (Q3 2024)

*   **Objetivo**: Incrementar la confiabilidad y calidad del proyecto.
*   **Iniciativas Clave**:
    *   **Implementar un Framework de Pruebas**: Introducir `pytest` para pruebas unitarias y de integración del backend.
    *   **CI/CD (Integración Continua)**: Configurar GitHub Actions para ejecutar pruebas automáticamente en cada commit.
    *   **Documentación para Desarrolladores**: Mejorar la documentación interna para facilitar nuevas contribuciones.
    *   **Sistema de "Health Check"**: Añadir un endpoint en la API que verifique la salud del sistema (conexión a internet, estado del micrófono, etc.).

### Épica 2: Mejorar la Experiencia de Usuario (Q4 2024)

*   **Objetivo**: Hacer la aplicación más intuitiva y personalizable.
*   **Iniciativas Clave**:
    *   **Personalización de la Interfaz**: Permitir a los usuarios cambiar el tamaño de la fuente, el contraste y los colores.
    *   **Soporte Multi-idioma**: Añadir soporte para transcripción en otros idiomas (ej. inglés, francés).
    *   **Feedback Visual Mejorado**: Mejorar la animación "Pulse" para que sea más clara y útil.
    *   **Modo Offline (Transcripción en el dispositivo)**: Investigar la viabilidad de usar modelos de transcripción locales para funcionar sin conexión a internet.

### Épica 3: Expandir el Ecosistema (2025)

*   **Objetivo**: Integrar Iyari-ear con otras herramientas y plataformas.
*   **Iniciativas Clave**:
    *   **API Pública**: Desarrollar una API documentada para que otros desarrolladores puedan integrar la tecnología de Iyari-ear en sus propias aplicaciones.
    *   **Integración con Plataformas de Streaming**: Crear extensiones para navegadores (ej. Chrome) para subtitular videos en vivo.
    *   **Aplicación de Escritorio Nativa**: Desarrollar una versión de escritorio (usando Electron o similar) para una experiencia más integrada en Windows, macOS y Linux.

## Timeline Proyectado

*   **Q3 2024**:
    *   Lanzamiento de la versión 1.0.
    *   Implementación completa de la Épica 1 (Robustecer y Validar).
*   **Q4 2024**:
    *   Desarrollo y lanzamiento de las mejoras de la Épica 2 (Experiencia de Usuario).
*   **2025 en adelante**:
    *   Investigación y desarrollo de la Épica 3 (Expandir el Ecosistema).
    *   Mantenimiento continuo y mejoras basadas en el feedback de la comunidad.

---

Este roadmap es un documento vivo y se actualizará a medida que el proyecto evolucione y la comunidad crezca.
