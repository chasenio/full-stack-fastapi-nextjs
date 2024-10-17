import typing as t
import yaml
import dacite
from dataclasses import dataclass
import consul


@dataclass
class Config:
    # database
    db_url: str

    # web api
    origins: t.List[str]  # cors origins

    port: int = 8000

    # application
    db_pool_size: t.Optional[int] = 20

    @classmethod
    def from_dict(cls, d: dict):
        return dacite.from_dict(
            cls, d,
        )

    @classmethod
    def from_file(cls, path: str) -> "Config":
        with open(path, 'r') as fp:
            return cls.from_dict(
                yaml.safe_load(fp.read())
            )

    @classmethod
    def from_consul(cls, consul_cfg: "ConsulConfig") -> "Config":

        client = consul.Consul(host=consul_cfg.host,
                               port=consul_cfg.port,
                               token=consul_cfg.token,
                               scheme=consul_cfg.schema)

        _, data = client.kv.get(consul_cfg.key)
        if not data:
            raise ValueError("config not found in consul")
        for k, v in data.items():
            if k != "Value":
                continue
            # Valur is bytes
            return cls.from_dict(yaml.safe_load(v))
        raise ValueError("config not found in consul")


@dataclass
class ConsulConfig:
    schema: str
    host: str
    token: str
    key: str
    port: t.Optional[int] = 443

    @classmethod
    def from_url(cls, consul_url: str) -> "ConsulConfig":
        """

        :param consul_url: is the fly.io consul url
                example
                    https://:xxx@consul-xxx.fly-shared.net/app-xxx/
        """
        _consul_items = consul_url.split("/")
        consul_items = [i for i in _consul_items if i]

        # schema, host, port, token
        schema = consul_items[0].split(":")[0]
        _token, host = consul_items[1].split("@")
        token = _token.strip(":")

        # parse key value
        # example:
        #    key = app-xxxxx/app
        #

        key_prefix = consul_items[-1]  # key_prefix is app-xxxxxxxx
        # app name is - split
        app_name_arr = key_prefix.split("-")[:-1]
        app_name = "-".join(app_name_arr)
        key = "/".join([key_prefix, app_name])
        return cls(schema=schema, host=host, token=token, key=key)


def load_cfg(config_path: str) -> Config:
    with open(config_path) as f:
        config_map = yaml.safe_load(f)
        return Config.from_dict(config_map)
