# TODO: IncubationApi
# FIXME: Get scopes to test this function


class IncubationApi:
    def get_cari_data(self, admin_level="admin0"):
        if admin_level == "admin0":
            pass
        elif admin_level == "admin1":
            pass
        else:
            raise ValueError("admin_level must be either 'admin0' or 'admin1'")
