import io
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

class ExportPDF:
    def generate(self, configuration):
        """
        Receives a Configuration object and return an in-memory buffer
        containing the generated PDF document.
        """

        # Create an in-memory buffer so we don't save physical files on the server
        buffer = io.BytesIO()

        # Configure the PDF document layout
        doc = SimpleDocTemplate(
            buffer,
            pagesize = A4,
            rightMargin = 54, leftMargin = 54, bottomMargin = 54
        )

        pdf_content = []
        styles = getSampleStyleSheet()

        # Define custome styles for an elegant invoice/offer look
        title_style = ParagraphStyle(
            'OfferTitle',
            parent=styles['Heading1'],
            fontSize=24,
            leading=28,
            textColor=colors.HexColor("#1A365D"), # Elegant dark blue
            spaceAfter=20
        )

        text_style = ParagraphStyle(
            'OfferText',
            parent=styles['Normal'],
            fontSize=12,
            leading=16,
            spaceAfter=10
        )

        price_style = ParagraphStyle(
            'OfferPrice',
            parent=styles['Normal'],
            fontSize=14,
            leading=18,
            textColor=colors.HexColor("#2F855A"), # Green for the total price
        )

        # Dynamically build the PDF content using database values
        pdf_content.append(Paragraph("CAR CONFIGURATION OFFER", title_style))
        pdf_content.append(Spacer(1, 12))

        pdf_content.append(Paragraph(f"<b>Client:</b> {configuration.user.username}", text_style))
        pdf_content.append(Paragraph(f"<b>Car Model:</b> {configuration.car_model.company_name} {configuration.car_model.model_name}", text_style))
        pdf_content.append(Spacer(1, 10))

        # Add the options selected by the user 
        pdf_content.append(Paragraph("<b>Selected Technical Specifications:</b>", text_style))

        
        engine_name = f"{configuration.engine.name} ({configuration.engine.power} HP)" if configuration.engine else "Not specified"
        bullet = "\u2022"
        pdf_content.append(Paragraph(f"{bullet} <b>Engine:</b> {engine_name}", text_style))

        color_name = configuration.color.name if configuration.color else "Not speciefied"
        pdf_content.append(Paragraph(f"{bullet} <b>Color:</b> {color_name}", text_style))

        wheels_name = f"{configuration.wheel.size}\" - {configuration.wheel.style}" if configuration.wheel else "Not specified"
        pdf_content.append(Paragraph(f"{bullet} <b>Wheels:</b> {wheels_name}", text_style))

        pdf_content.append(Spacer(1, 15))
        
        # Calculate and display the total price
        pdf_content.append(Paragraph(f"<b>Estimated Total Price:</b> {configuration.total_price()} EUR", price_style))

        # Build the document
        doc.build(pdf_content)

        # Reset the buffer pointer to the begining so Django can read it properly
        buffer.seek(0)
        return buffer