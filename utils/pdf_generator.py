"""PDF Generator for Museum Exhibitions using HTML."""
from io import BytesIO
from datetime import datetime

class ExhibitionPDFGenerator:
    """Generate professional HTML-based PDF documents for exhibitions."""
    
    def __init__(self):
        pass
    
    def generate_pdf(self, exhibition: dict, metrics: dict = None) -> str:
        """Generate HTML content that can be printed as PDF."""
        html = self._generate_html(exhibition, metrics)
        return html
    
    def _generate_html(self, exhibition: dict, metrics: dict = None) -> str:
        """Generate styled HTML for PDF export."""
        title = exhibition.get('title', exhibition.get('topic', 'Museum Exhibition'))
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        @page {{
            size: A4;
            margin: 2cm;
        }}
        body {{
            font-family: 'Georgia', serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }}
        .title-page {{
            text-align: center;
            padding: 60px 0;
            page-break-after: always;
        }}
        .title {{
            font-size: 36px;
            color: #1E3A8A;
            margin: 20px 0;
            font-weight: bold;
        }}
        .subtitle {{
            font-size: 18px;
            color: #6B7280;
            margin: 15px 0;
        }}
        .metrics {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 30px 0;
            padding: 20px;
            background: #EFF6FF;
            border-radius: 8px;
        }}
        .metric {{
            text-align: center;
            padding: 10px;
        }}
        .metric-label {{
            font-size: 12px;
            color: #6B7280;
            text-transform: uppercase;
        }}
        .metric-value {{
            font-size: 24px;
            color: #1E3A8A;
            font-weight: bold;
        }}
        .curator-notes {{
            background: #F9FAFB;
            padding: 30px;
            margin: 30px 0;
            border-left: 4px solid #3B82F6;
            font-style: italic;
            page-break-after: always;
        }}
        .room {{
            margin: 40px 0;
            page-break-inside: avoid;
        }}
        .room-title {{
            font-size: 24px;
            color: #3B82F6;
            margin: 20px 0 10px 0;
            border-bottom: 2px solid #3B82F6;
            padding-bottom: 10px;
        }}
        .room-theme {{
            font-size: 14px;
            color: #6B7280;
            font-weight: bold;
            margin: 10px 0;
        }}
        .room-description {{
            margin: 15px 0;
            color: #374151;
        }}
        .exhibit {{
            margin: 25px 0 25px 20px;
            padding: 20px;
            background: #F9FAFB;
            border-radius: 8px;
            page-break-inside: avoid;
        }}
        .exhibit-title {{
            font-size: 18px;
            color: #1E3A8A;
            margin-bottom: 10px;
            font-weight: bold;
        }}
        .exhibit-period {{
            font-size: 12px;
            color: #6B7280;
            font-style: italic;
            margin-bottom: 10px;
        }}
        .exhibit-description {{
            margin: 10px 0;
            text-align: justify;
        }}
        .significance {{
            margin: 15px 0;
            padding: 10px;
            background: #FEF3C7;
            border-left: 3px solid #F59E0B;
        }}
        .facts {{
            margin: 15px 0;
        }}
        .fact {{
            margin: 5px 0 5px 20px;
            color: #374151;
        }}
        .timeline {{
            margin: 40px 0;
            page-break-before: always;
        }}
        .timeline-title {{
            font-size: 28px;
            color: #1E3A8A;
            margin-bottom: 30px;
            text-align: center;
        }}
        .timeline-event {{
            margin: 20px 0;
            padding-left: 30px;
            border-left: 3px solid #D4AF37;
            position: relative;
        }}
        .timeline-year {{
            font-size: 18px;
            color: #1E3A8A;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        .timeline-description {{
            color: #374151;
        }}
        .footer {{
            text-align: center;
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #E5E7EB;
            color: #9CA3AF;
            font-size: 12px;
        }}
        @media print {{
            body {{ margin: 0; }}
            .page-break {{ page-break-after: always; }}
        }}
    </style>
</head>
<body>
    <div class="title-page">
        <div style="font-size: 48px;">🏛️</div>
        <h1 class="title">{title}</h1>
        <p class="subtitle">{exhibition.get('overview', '')}</p>
        
        {self._generate_metrics_html(metrics) if metrics else ''}
        
        <div class="footer">
            Generated by AI Museum Curator<br>
            {datetime.now().strftime('%B %d, %Y')}
        </div>
    </div>
    
    {self._generate_curator_notes_html(exhibition)}
    
    {self._generate_rooms_html(exhibition)}
    
    {self._generate_timeline_html(exhibition)}
    
</body>
</html>
"""
        return html
    
    def _generate_metrics_html(self, metrics: dict) -> str:
        """Generate metrics HTML."""
        return f"""
        <div class="metrics">
            <div class="metric">
                <div class="metric-label">Quality Score</div>
                <div class="metric-value">{metrics.get('overall_quality_score', 0)*100:.1f}%</div>
            </div>
            <div class="metric">
                <div class="metric-label">Success Rate</div>
                <div class="metric-value">{metrics.get('agent_success_rate', 0)*100:.1f}%</div>
            </div>
            <div class="metric">
                <div class="metric-label">Narrative Quality</div>
                <div class="metric-value">{metrics.get('narrative_quality', 0)*100:.1f}%</div>
            </div>
            <div class="metric">
                <div class="metric-label">Cultural Sensitivity</div>
                <div class="metric-value">{metrics.get('cultural_sensitivity', 0)*100:.1f}%</div>
            </div>
        </div>
        """
    
    def _generate_curator_notes_html(self, exhibition: dict) -> str:
        """Generate curator notes HTML."""
        notes = exhibition.get('curator_notes', '')
        if not notes:
            return ''
        
        return f"""
        <div class="curator-notes">
            <h2>Curator's Notes</h2>
            <p>{notes}</p>
        </div>
        """
    
    def _generate_rooms_html(self, exhibition: dict) -> str:
        """Generate rooms HTML."""
        html = ''
        for i, room in enumerate(exhibition.get('rooms', []), 1):
            html += f"""
            <div class="room">
                <h2 class="room-title">Room {i}: {room.get('title', 'Untitled')}</h2>
                <div class="room-theme">Theme: {room.get('theme', 'N/A')}</div>
                <div class="room-description">{room.get('description', '')}</div>
                {f'<p><em>{room.get("narrative", "")}</em></p>' if room.get('narrative') else ''}
                
                {self._generate_exhibits_html(room.get('exhibits', []))}
            </div>
            """
        return html
    
    def _generate_exhibits_html(self, exhibits: list) -> str:
        """Generate exhibits HTML."""
        html = ''
        for j, exhibit in enumerate(exhibits, 1):
            facts_html = ''
            if exhibit.get('facts'):
                facts_html = '<div class="facts"><strong>Interesting Facts:</strong>'
                for fact in exhibit['facts'][:5]:
                    facts_html += f'<div class="fact">• {fact}</div>'
                facts_html += '</div>'
            
            html += f"""
            <div class="exhibit">
                <div class="exhibit-title">Exhibit {j}: {exhibit.get('name', 'Untitled')}</div>
                {f'<div class="exhibit-period">Time Period: {exhibit.get("time_period", "")}</div>' if exhibit.get('time_period') else ''}
                <div class="exhibit-description">{exhibit.get('description', '')}</div>
                {f'<div class="significance"><strong>Cultural Significance:</strong> {exhibit.get("cultural_significance", "")}</div>' if exhibit.get('cultural_significance') else ''}
                {facts_html}
            </div>
            """
        return html
    
    def _generate_timeline_html(self, exhibition: dict) -> str:
        """Generate timeline HTML."""
        timeline = exhibition.get('timeline', [])
        if not timeline:
            return ''
        
        html = '<div class="timeline"><h2 class="timeline-title">Historical Timeline</h2>'
        for event in timeline[:15]:
            html += f"""
            <div class="timeline-event">
                <div class="timeline-year">{event.get('year', 'Unknown')}</div>
                <div class="timeline-description">
                    <strong>{event.get('event', 'Event')}</strong>: {event.get('description', '')}
                </div>
            </div>
            """
        html += '</div>'
        return html
    

