docker run -d --restart always --net=host \
-v $PWD/config/rabbitmq/rabbitmq.conf:/etc/rabbitmq/rabbitmq.conf \
-v $PWD/config/rabbitmq/cert.cer:/etc/cert.cer \
-v $PWD/config/rabbitmq/key.pem:/etc/key.pem \
--name rabbitmq rabbitmq:3.7.0
