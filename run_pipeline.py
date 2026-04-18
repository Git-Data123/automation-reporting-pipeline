import sys
from datetime import datetime
from pathlib import Path
from src.ingest import load_data
from src.logger_config import setup_logger
from src.validate import validate_data
from dotenv import load_dotenv
import os
from src.emailer import send_email_with_attachment
from src.transform import (
    transform_data,
    calculate_kpis,
    calculate_region_summary,
    calculate_product_summary,
)
from src.report import generate_report, export_to_excel


def main():
    """
    Run the full financial reporting pipeline.
    """
    load_dotenv()
    logger = None

    try:
        project_root = Path(__file__).resolve().parent

        # Use command-line input if provided, otherwise use default file
        if len(sys.argv) > 1:
            input_file = Path(sys.argv[1])
            if not input_file.is_absolute():
                input_file = project_root / input_file
        else:
            input_file = project_root / "data" / "raw" / "sales_data.csv"

        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")

        output_dir = project_root / "output"
        text_output_file = output_dir / f"financial_report_{timestamp}.txt"
        excel_output_file = output_dir / f"financial_report_{timestamp}.xlsx"
        log_file = output_dir / f"pipeline_log_{timestamp}.log"
        output_dir.mkdir(parents=True, exist_ok=True)
        logger = setup_logger(log_file)

        # Email settings from environment variables
        smtp_server = os.getenv("SMTP_SERVER")
        smtp_port = int(os.getenv("SMTP_PORT", 587))
        sender_email = os.getenv("SENDER_EMAIL")
        sender_password = os.getenv("SENDER_PASSWORD")
        recipient_email = os.getenv("RECIPIENT_EMAIL")

        if not all([smtp_server, sender_email, sender_password, recipient_email]):
            raise ValueError("Missing one or more email environment variables.")

        logger.info("Starting financial reporting pipeline...")
        logger.info(f"Using input file: {input_file}")

        # Step 1: Load data
        df = load_data(input_file)

        # Step 2: Validate data
        validate_data(df)

        # Step 3: Transform data
        transformed_df = transform_data(df)

        # Step 4: Calculate KPIs
        kpis = calculate_kpis(transformed_df)
        region_summary = calculate_region_summary(transformed_df)
        product_summary = calculate_product_summary(transformed_df)

        # Step 5: Generate text report
        report = generate_report(kpis, region_summary, product_summary)

        # Step 6: Print report
        logger.info("Financial report generated successfully.")
        logger.info("\n" + report)

        # Step 7: Ensure output folder exists
        output_dir.mkdir(parents=True, exist_ok=True)

        # Step 8: Save text report
        with open(text_output_file, "w", encoding="utf-8") as file:
            file.write(report)

        # Step 9: Save Excel report
        export_to_excel(
            transformed_df,
            kpis,
            region_summary,
            product_summary,
            excel_output_file,
        )

        # Step 10: Send email with Excel attachment
        email_subject = "Automated Financial Report"
        email_body = (
            "Hello,\n\n"
            "Please find attached the latest automated financial report.\n\n"
            "Regards,\n"
            "Financial Reporting Pipeline"
        )

        send_email_with_attachment(
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            sender_email=sender_email,
            sender_password=sender_password,
            recipient_email=recipient_email,
            subject=email_subject,
            body=email_body,
            attachment_path=excel_output_file,
        )

        logger.info(f"Text report saved to: {text_output_file}")
        logger.info(f"Excel report saved to: {excel_output_file}")
        logger.info(f"Email sent to: {recipient_email}")
        logger.info("Pipeline completed successfully.")

    except Exception as e:
        if logger:
            logger.exception(f"Pipeline failed: {e}")
        else:
            print(f"Pipeline failed before logger setup: {e}")

if __name__ == "__main__":
    main()