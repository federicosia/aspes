from app.domain.service.category import create_category, delete_category, get_category


def test_get_category(fake_uow):
    with fake_uow:
        category = create_category(
            fake_uow, name="Test Category", description="A test category"
        )
        assert category is not None
        assert category.id is not None
        category_res = get_category(fake_uow, category.id)
        assert category_res is not None
        assert category_res.id == category.id
        assert category_res.name == category.name
        assert category_res.description == category.description


def test_create_category(fake_uow):
    with fake_uow:
        category = create_category(
            fake_uow, name="Test Category", description="A test category"
        )
        assert category is not None
        assert category.id is not None
        assert category.name == "Test Category"
        assert category.description == "A test category"


def test_delete_category(fake_uow):
    with fake_uow:
        category = create_category(
            fake_uow, name="Test Category", description="A test category"
        )
        assert category is not None
        assert category.id is not None
        delete_category(fake_uow, category.id)
        assert get_category(fake_uow, category.id) is None
