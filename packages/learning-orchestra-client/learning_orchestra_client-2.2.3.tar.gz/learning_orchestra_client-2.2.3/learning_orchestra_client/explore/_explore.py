from learning_orchestra_client.observe.observe import Observer
from learning_orchestra_client._util._response_treat import ResponseTreat
from learning_orchestra_client._util._entity_reader import EntityReader
import requests
from typing import Union


class Explore:
    __PARENT_NAME_FIELD = "parentName"
    __MODEL_NAME_FIELD = "modelName"
    __METHOD_NAME_FIELD = "method"
    __ClASS_PARAMETERS_FIELD = "methodParameters"
    __NAME_FIELD = "name"
    __DESCRIPTION_FIELD = "description"

    def __init__(self, cluster_ip: str, api_path: str):
        self.__service_url = f'{cluster_ip}{api_path}'
        self.__response_treat = ResponseTreat()
        self.__cluster_ip = cluster_ip
        self.__entity_reader = EntityReader(self.__service_url)
        self.__observer = Observer(self.__cluster_ip)

    def create_explore_sync(self,
                            name: str,
                            model_name: str,
                            parent_name: str,
                            method_name: str,
                            parameters: dict,
                            description: str = "",
                            pretty_response: bool = False) -> \
            Union[dict, str]:
        """
        description: This method runs an evaluation about a model in sync mode

        pretty_response: If true it returns a string, otherwise a dictionary.
        name: Is the name of the model that will be explored.
        parent_name: The name of the previous pipe in the pipeline
        method_name: the name of the ML tool method used to explore a model
        parameters: the set of parameters of the ML method defined previously

        return: A JSON object with an error or warning message or a URL
        indicating the correct operation.
        """
        request_body = {
            self.__NAME_FIELD: name,
            self.__MODEL_NAME_FIELD: model_name,
            self.__PARENT_NAME_FIELD: parent_name,
            self.__METHOD_NAME_FIELD: method_name,
            self.__ClASS_PARAMETERS_FIELD: parameters,
            self.__DESCRIPTION_FIELD: description}

        request_url = self.__service_url

        response = requests.post(url=request_url, json=request_body)
        self.__observer.wait(name)

        return self.__response_treat.treatment(response, pretty_response)

    def create_explore_async(self,
                             name: str,
                             model_name: str,
                             parent_name: str,
                             method_name: str,
                             parameters: dict,
                             description: str = "",
                             pretty_response: bool = False) -> \
            Union[dict, str]:
        """
        description: This method runs an explore service about a model in async
        mode

        pretty_response: If true it returns a string, otherwise a dictionary.
        name: Is the name of the model that will be explored.
        parent_name: The name of the previous pipe in the pipeline
        method_name: the name of the ML tool method used to explore a model
        parameters: the set of parameters of the ML method defined previously

        return: A JSON object with an error or warning message or a URL
        indicating the correct operation.
        """
        request_body = {
            self.__NAME_FIELD: name,
            self.__MODEL_NAME_FIELD: model_name,
            self.__PARENT_NAME_FIELD: parent_name,
            self.__METHOD_NAME_FIELD: method_name,
            self.__ClASS_PARAMETERS_FIELD: parameters,
            self.__DESCRIPTION_FIELD: description}

        request_url = self.__service_url

        response = requests.post(url=request_url, json=request_body)
        return self.__response_treat.treatment(response, pretty_response)

    def search_all_explores(self, pretty_response: bool = False) \
            -> Union[dict, str]:
        """
        description: This method retrieves all created explorations, i.e., it
        does not retrieve the specific explore content.

        pretty_response: If true it returns a string, otherwise a dictionary.

        return: All datasets metadata stored in Learning Orchestra or an empty
        result.
        """
        response = self.__entity_reader.read_all_instances_from_entity()
        return self.__response_treat.treatment(response, pretty_response)

    def delete_explore(self, name: str, pretty_response=False) \
            -> Union[dict, str]:
        """
        description: This method is responsible for deleting an explore result.
        This delete operation is asynchronous, so it does not lock the caller
         until the deletion finished. Instead, it returns a JSON object with a
         URL for a future use. The caller uses the wait method for delete
         checks. If a dataset was used by another task (Ex. projection,
         histogram, tune and so forth), it cannot be deleted.

        pretty_response: If true it returns a string, otherwise a dictionary.
        name: Represents the model name.

        return: JSON object with an error message, a warning message or a
        correct delete message
        """

        request_url = f'{self.__service_url}/{name}'

        response = requests.delete(request_url)
        return self.__response_treat.treatment(response, pretty_response)

    def search_explore_image(self,
                             name: str,
                             pretty_response: bool = False) \
            -> Union[dict, str]:
        """
        description:  This method is responsible for retrieving the explore
        image to be plotted

        pretty_response: If true it returns a string, otherwise a dictionary.
        name: Is the name of the explore instance.

        return: An URL with a link for an image or an error if there
        is no such result.
        """

        response = self.__entity_reader.read_entity_content(
            name)

        return self.__response_treat.treatment(response, pretty_response)

    def search_explore_metadata(self,
                                name: str,
                                pretty_response: bool = False) \
            -> Union[dict, str]:
        """
        description:  This method is responsible for retrieving the explore
        metadata image.

        pretty_response: If true it returns a string, otherwise a dictionary.
        name: Is the name of the explore instance.

        return: A page with some metadata inside or an error if there
        is no such dataset. The current page is also returned to be used in
        future content requests.
        """

        response = self.__entity_reader.read_explore_image_metadata(name)

        return self.__response_treat.treatment(response, pretty_response)

    def wait(self, name: str, timeout: int = None) -> dict:
        """
       description: This method is responsible to create a synchronization
       barrier for the create_explore_async method, delete_explore_async
       method.

       name: Represents the model name.
       timeout: Represents the time in seconds to wait for an explore to
       finish its run.

       return: JSON object with an error message, a warning message or a
       correct explore result (the image URL as an explore result)
        """
        return self.__observer.wait(name, timeout)
