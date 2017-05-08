# ele_services

> 华师匣子电费查询服务

## 环境配置(container.env)

    MONGOHOST='localhost' // mongodb host
    MONGOPORT='27017'     // mongodb port

## 部署

**单独部署**:

```shell
$ docker-compose stop && docker-compose build && dockder-compose up -d &&
docker-compose ps
```

## 测试

+ 配置```container.test.env```

```shell
$./start_test.sh && docker-compose -f docker-compose.test.yml logs --tail="100" mana_api_test
```

## Log

+ 2017年4月29日: 拖了2个月了...ㄟ( ▔, ▔ )ㄏ
