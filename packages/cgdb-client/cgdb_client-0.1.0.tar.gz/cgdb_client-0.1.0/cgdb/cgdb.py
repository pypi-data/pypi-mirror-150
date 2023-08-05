from cgdb.managers import AggregationsManager
from cgdb.managers import ElementsManager
from cgdb.managers import FlagListManager
from cgdb.managers import SitesManager
from cgdb.managers import DataSetsManager
from cgdb.managers import StationNetworksManager
from cgdb.managers import TimeStepsManager
from cgdb.recources import Site
from cgdb.managers import DepartmentsManager
from cgdb.managers import ElementsCategoriesManager
from cgdb.managers import ParametersManager
from cgdb.managers import ElementContextsManager

from cgdb.utils import CGDBAPISession
import urllib3
urllib3.disable_warnings()

class CGDB:
    """Client to bundle configuration needed for API requests.
        :type api_key: str
        :param api_key: api key for authenticate to api endpoint

        :type host: str or None
        :param host: api endpoint url
    """
    def __init__(self, api_key, host=None):
        if host is None:
            host = "https://localhost:8443/api/"
        self._session = CGDBAPISession(host, api_key)
        self._sites_manager = SitesManager(client=self)
        self._data_sets_manager = DataSetsManager(client=self)
        self._departments_manager = DepartmentsManager(client=self)
        self._elements_manager = ElementsManager(client=self)
        self._elements_categories_manager = ElementsCategoriesManager(client=self)
        self._flag_lists_manager = FlagListManager(client=self)
        self._parameters_manager = ParametersManager(client=self)
        self._time_steps_manager = TimeStepsManager(client=self)
        self._element_contexts_manager = ElementContextsManager(client=self)
        self._station_networks_manager = StationNetworksManager(client=self)
        self._aggregations_manager = AggregationsManager()

    def sites(self):
        return self._sites_manager.sites()

    def site(self, mark) -> Site:
        return self._sites_manager.site(mark)

    def departments(self):
        return self._departments_manager.departments()

    def department(self, id: str):
        return self._departments_manager.department(id)

    def elements(self):
        return self._elements_manager.elements()

    def element(self, mark: str):
        return self._elements_manager.element(mark)

    def element_contexts(self):
        return self._element_contexts_manager.element_contexts()

    def time_steps(self):
        return self._time_steps_manager.time_steps()

    def time_step_by_code(self, code):
        return self._time_steps_manager.time_step_by_code(code)

    def time_step_by_id(self, id):
        return self._time_steps_manager.time_step_by_id(id)

    def aggregations(self):
        return self._aggregations_manager.aggregations()

    def create_data_set(self, station, element_code, aggregation, time_step_code, data_set_type):
        self._data_sets_manager.create_data_set(station, element_code, aggregation, time_step_code, data_set_type)

    def create_station(self, name, code, gpsLatitude, gpsLongitude, altitude, stationNetworkCode, remark=""):
        self._sites_manager.create_station(name, code, gpsLatitude, gpsLongitude, altitude, stationNetworkCode, remark)