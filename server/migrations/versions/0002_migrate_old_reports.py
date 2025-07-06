"""Migrate old reports to new schema

Revision ID: 0002
Revises: 0001
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Check if old columns exist (for existing databases)
    connection = op.get_bind()
    
    # Check if report_data column exists
    inspector = sa.inspect(connection)
    columns = [col['name'] for col in inspector.get_columns('user_reports')]
    
    if 'report_data' in columns:
        # Migrate existing data from report_data to jobs_data
        op.execute("""
            UPDATE user_reports 
            SET jobs_data = report_data,
                job_count = CASE 
                    WHEN report_data IS NOT NULL AND report_data != '' 
                    THEN json_array_length(report_data::json)
                    ELSE 0 
                END
            WHERE report_data IS NOT NULL
        """)
        
        # Drop old columns
        op.drop_column('user_reports', 'report_data')
        op.drop_column('user_reports', 'report_type')


def downgrade() -> None:
    # Add back old columns
    op.add_column('user_reports', sa.Column('report_data', sa.Text(), nullable=True))
    op.add_column('user_reports', sa.Column('report_type', sa.String(length=50), nullable=True))
    
    # Restore data
    op.execute("""
        UPDATE user_reports 
        SET report_data = jobs_data,
            report_type = 'job_search'
        WHERE jobs_data IS NOT NULL
    """)
    
    # Drop new columns
    op.drop_column('user_reports', 'jobs_data')
    op.drop_column('user_reports', 'keyword')
    op.drop_column('user_reports', 'sources_used')
    op.drop_column('user_reports', 'job_count') 