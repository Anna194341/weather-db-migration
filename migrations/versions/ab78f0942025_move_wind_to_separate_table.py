"""move wind to separate table

Revision ID: ab78f0942025
Revises: 1458787a732c
Create Date: 2026-04-26 23:20:07.847553

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ab78f0942025'
down_revision: Union[str, Sequence[str], None] = '1458787a732c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.create_table(
        'wind',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('wind_mph', sa.Float(), nullable=True),
        sa.Column('wind_kph', sa.Float(), nullable=True),
        sa.Column('wind_degree', sa.Integer(), nullable=True),
        sa.Column(
            'wind_direction',
            sa.Enum(
                'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW',
                name='winddirection',
                create_type=False
            ),
            nullable=True
        ),
        sa.Column('gust_mph', sa.Float(), nullable=True),
        sa.Column('gust_kph', sa.Float(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_wind_id'), 'wind', ['id'], unique=False)

    op.add_column('weather', sa.Column('wind_id', sa.Integer(), nullable=True))

    op.execute("""
        INSERT INTO wind (
            wind_mph,
            wind_kph,
            wind_degree,
            wind_direction,
            gust_mph,
            gust_kph
        )
        SELECT
            wind_mph,
            wind_kph,
            wind_degree,
            wind_direction,
            gust_mph,
            gust_kph
        FROM weather
        ORDER BY id
    """)

    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "mysql":
        op.execute("""
            UPDATE weather
            JOIN wind ON wind.id = weather.id
            SET weather.wind_id = wind.id
        """)
    else:
        op.execute("""
            UPDATE weather
            SET wind_id = wind.id
            FROM wind
            WHERE wind.id = weather.id
        """)

    op.create_foreign_key(
        'fk_weather_wind',
        'weather',
        'wind',
        ['wind_id'],
        ['id']
    )

    op.drop_column('weather', 'wind_degree')
    op.drop_column('weather', 'gust_kph')
    op.drop_column('weather', 'gust_mph')
    op.drop_column('weather', 'wind_mph')
    op.drop_column('weather', 'wind_kph')
    op.drop_column('weather', 'wind_direction')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""

    op.add_column(
        'weather',
        sa.Column(
            'wind_direction',
            sa.Enum(
                'N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE',
                'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW',
                name='winddirection',
                create_type=False
            ),
            nullable=True
        )
    )
    op.add_column('weather', sa.Column('wind_kph', sa.Float(), nullable=True))
    op.add_column('weather', sa.Column('wind_mph', sa.Float(), nullable=True))
    op.add_column('weather', sa.Column('gust_mph', sa.Float(), nullable=True))
    op.add_column('weather', sa.Column('gust_kph', sa.Float(), nullable=True))
    op.add_column('weather', sa.Column('wind_degree', sa.Integer(), nullable=True))

    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "mysql":
        op.execute("""
            UPDATE weather
            JOIN wind ON weather.wind_id = wind.id
            SET
                weather.wind_mph = wind.wind_mph,
                weather.wind_kph = wind.wind_kph,
                weather.wind_degree = wind.wind_degree,
                weather.wind_direction = wind.wind_direction,
                weather.gust_mph = wind.gust_mph,
                weather.gust_kph = wind.gust_kph
        """)
    else:
        op.execute("""
            UPDATE weather
            SET
                wind_mph = wind.wind_mph,
                wind_kph = wind.wind_kph,
                wind_degree = wind.wind_degree,
                wind_direction = wind.wind_direction,
                gust_mph = wind.gust_mph,
                gust_kph = wind.gust_kph
            FROM wind
            WHERE weather.wind_id = wind.id
        """)

    op.drop_constraint('fk_weather_wind', 'weather', type_='foreignkey')
    op.drop_column('weather', 'wind_id')
    op.drop_index(op.f('ix_wind_id'), table_name='wind')
    op.drop_table('wind')
    # ### end Alembic commands ###
