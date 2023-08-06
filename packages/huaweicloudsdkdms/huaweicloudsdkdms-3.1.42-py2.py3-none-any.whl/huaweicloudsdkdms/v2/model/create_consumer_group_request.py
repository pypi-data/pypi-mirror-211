# coding: utf-8

import six

from huaweicloudsdkcore.utils.http_utils import sanitize_for_serialization


class CreateConsumerGroupRequest:

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    sensitive_list = []

    openapi_types = {
        'queue_id': 'str',
        'body': 'CreateConsumerGroupReq'
    }

    attribute_map = {
        'queue_id': 'queue_id',
        'body': 'body'
    }

    def __init__(self, queue_id=None, body=None):
        """CreateConsumerGroupRequest

        The model defined in huaweicloud sdk

        :param queue_id: 指定的队列ID
        :type queue_id: str
        :param body: Body of the CreateConsumerGroupRequest
        :type body: :class:`huaweicloudsdkdms.v2.CreateConsumerGroupReq`
        """
        
        

        self._queue_id = None
        self._body = None
        self.discriminator = None

        self.queue_id = queue_id
        if body is not None:
            self.body = body

    @property
    def queue_id(self):
        """Gets the queue_id of this CreateConsumerGroupRequest.

        指定的队列ID

        :return: The queue_id of this CreateConsumerGroupRequest.
        :rtype: str
        """
        return self._queue_id

    @queue_id.setter
    def queue_id(self, queue_id):
        """Sets the queue_id of this CreateConsumerGroupRequest.

        指定的队列ID

        :param queue_id: The queue_id of this CreateConsumerGroupRequest.
        :type queue_id: str
        """
        self._queue_id = queue_id

    @property
    def body(self):
        """Gets the body of this CreateConsumerGroupRequest.

        :return: The body of this CreateConsumerGroupRequest.
        :rtype: :class:`huaweicloudsdkdms.v2.CreateConsumerGroupReq`
        """
        return self._body

    @body.setter
    def body(self, body):
        """Sets the body of this CreateConsumerGroupRequest.

        :param body: The body of this CreateConsumerGroupRequest.
        :type body: :class:`huaweicloudsdkdms.v2.CreateConsumerGroupReq`
        """
        self._body = body

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                if attr in self.sensitive_list:
                    result[attr] = "****"
                else:
                    result[attr] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        import simplejson as json
        if six.PY2:
            import sys
            reload(sys)
            sys.setdefaultencoding("utf-8")
        return json.dumps(sanitize_for_serialization(self), ensure_ascii=False)

    def __repr__(self):
        """For `print`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, CreateConsumerGroupRequest):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
