/etc/hosts
172.21.42.150 jg2bmp6z63.execute-api.ap-northeast-1.amazonaws.com

curl -D -  https://jg2bmp6z63.execute-api.ap-northeast-1.amazonaws.com/dev/aws/apply --data 'hello'


{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::173062506398:role/desmond.cao"
            },
            "Action": "execute-api:Invoke",
            "Resource": "arn:aws:execute-api:ap-northeast-1:173062506398:jg2bmp6z63/*/*/*"
        },
        {
            "Effect": "Deny",
            "Principal": "*",
            "Action": "execute-api:Invoke",
            "Resource": "arn:aws:execute-api:ap-northeast-1:173062506398:jg2bmp6z63/*/*/*",
            "Condition": {
                "StringNotEquals": {
                    "aws:SourceVpce": "vpce-079945d81eb006c99"
                }
            }
        }
    ]
}