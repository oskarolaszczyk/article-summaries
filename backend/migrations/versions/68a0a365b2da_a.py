"""a

Revision ID: 68a0a365b2da
Revises: f536a1eb5e8c
Create Date: 2024-05-16 19:50:33.952361

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68a0a365b2da'
down_revision = 'f536a1eb5e8c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('articles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.Column('source_url', sa.String(), nullable=False),
    sa.Column('date_added', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('summaries',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('article_id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('rating', sa.Boolean(), nullable=True),
    sa.Column('model_type', sa.Enum('MEANINGCLOUD', 'OUR_MODEL', name='modeltype'), nullable=False),
    sa.Column('date_generated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['articles.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('summaries')
    op.drop_table('articles')
    # ### end Alembic commands ###
