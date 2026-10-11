import pytest
from sqlalchemy import text

from app import create_app
from app.extensions import db


@pytest.fixture
def menu_client():
    app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite://",
            "SQLALCHEMY_ENGINE_OPTIONS": {},
            "JWT_SECRET_KEY": "test-secret",
        }
    )

    with app.app_context():
        db.session.execute(
            text(
                """
                CREATE TABLE menu (
                    id INTEGER PRIMARY KEY,
                    nama_menu VARCHAR(150) NOT NULL,
                    rasa VARCHAR(20),
                    id_produksi BIGINT,
                    id_sppg BIGINT NOT NULL,
                    kalori_kcal INTEGER,
                    biaya_per_porsi NUMERIC(10, 2),
                    is_halal BOOLEAN,
                    kategori_gizi VARCHAR(50),
                    created_at DATETIME,
                    updated_at DATETIME
                )
                """
            )
        )
        db.session.execute(
            text(
                """
                INSERT INTO menu (id, nama_menu, rasa, id_sppg, is_halal)
                VALUES
                    (1, 'Menu gurih', 'Gurih', 2, 1),
                    (2, 'Menu manis', 'Manis', 3, 0)
                """
            )
        )
        db.session.commit()

    yield app.test_client()

    with app.app_context():
        db.session.execute(text("DROP TABLE menu"))
        db.session.commit()


def test_daftar_returns_menu_and_filters(menu_client):
    response = menu_client.get("/menu?id_sppg=2&is_halal=true")

    assert response.status_code == 200
    body = response.get_json()
    assert [item["id"] for item in body["data"]] == [1]
    assert body["meta"]["total"] == 1


@pytest.mark.parametrize("id_sppg", ["abc", "0", "-1"])
def test_daftar_rejects_invalid_id_sppg(menu_client, id_sppg):
    response = menu_client.get(f"/menu?id_sppg={id_sppg}")

    assert response.status_code == 422
    assert response.get_json()["errors"]["id_sppg"] == (
        "harus berupa bilangan bulat positif"
    )
