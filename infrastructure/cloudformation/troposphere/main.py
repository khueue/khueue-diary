import troposphere
import troposphere.cloudfront

CONFIG = {
	'public': {
		'domain_names': [
			'khueue.com',
		],
	},
	'origin': {
		'domain_name': 'khueue-diary-app.s3-website-eu-west-1.amazonaws.com',
	},
	'log_bucket': {
		'name': 'khueue-diary-logs',
		'prefix': 'app-cloudfront/',
	},
	'ssl_certificate_arn': 'arn:aws:acm:us-east-1:682695698822:certificate/38e9e96c-7607-48a1-861c-9d4e968c7251',
}

template = troposphere.Template()

custom_error_responses = []
# Redirect all 404s to the app.
custom_error_responses.append(
	troposphere.cloudfront.CustomErrorResponse(
		ErrorCachingMinTTL=0,
		ErrorCode=404,
		ResponseCode=200,
		ResponsePagePath='/index.html',
	)
)
for error_code in [400, 403, 405, 414, 416] + [500, 501, 502, 503, 504]:
	custom_error = troposphere.cloudfront.CustomErrorResponse(
		ErrorCachingMinTTL=3,
		ErrorCode=error_code,
	)
	custom_error_responses.append(custom_error)

cloudfront_distribution = troposphere.cloudfront.Distribution(
	'CloudFrontDistribution',
	template=template,
	DistributionConfig=troposphere.cloudfront.DistributionConfig(
		Enabled=True,
		PriceClass='PriceClass_100',
		Aliases=CONFIG['public']['domain_names'],
		Origins=[
			troposphere.cloudfront.Origin(
				Id='origin',
				DomainName=CONFIG['origin']['domain_name'],
				CustomOriginConfig=troposphere.cloudfront.CustomOrigin(
					OriginProtocolPolicy='http-only',
				),
			),
		],
		HttpVersion='http2',
		IPV6Enabled=True,
		ViewerCertificate=troposphere.cloudfront.ViewerCertificate(
			AcmCertificateArn=CONFIG['ssl_certificate_arn'],
			SslSupportMethod='sni-only',
			MinimumProtocolVersion='TLSv1.2_2018',
		),
		DefaultRootObject='index.html',
		CustomErrorResponses=custom_error_responses,
		DefaultCacheBehavior=troposphere.cloudfront.DefaultCacheBehavior(
			ViewerProtocolPolicy='redirect-to-https',
			AllowedMethods=[
				'GET',
				'HEAD',
			],
			CachedMethods=[
				'GET',
				'HEAD',
			],
			Compress=True,
			DefaultTTL=10,
			MinTTL=0,
			MaxTTL=60*60*24*365,
			TargetOriginId='origin',
			ForwardedValues=troposphere.cloudfront.ForwardedValues(
				QueryString=False,
				Headers=[],
				Cookies=troposphere.cloudfront.Cookies(
					Forward='none',
				),
			),
		),
		Logging=troposphere.cloudfront.Logging(
			Bucket=CONFIG['log_bucket']['name'] + '.s3.amazonaws.com',
			Prefix=CONFIG['log_bucket']['prefix'],
			IncludeCookies=True,
		),
	),
)

print(template.to_json())
