import troposphere
import troposphere.route53

CONFIG = {
	'public': {
		'hosted_zone_name': 'khueue.com',
		'domain_names': [
			'khueue.com',
		],
	},
	'target': {
		'domain_name': 'dqhvp77ter579.cloudfront.net',
		'cloudfront_hosted_zone_id': 'Z2FDTNDATAQYW2', # Fixed ID for CloudFront.
	},
}

template = troposphere.Template()

hosted_zone = troposphere.route53.HostedZone(
	'HostedZone',
	template=template,
	Name=CONFIG['public']['hosted_zone_name'] + '.',
)

record_sets = []

record_set = troposphere.route53.RecordSet(
	Name='mage.khueue.com.',
	Type='NS',
	TTL=300,
	ResourceRecords=[
		'ns-826.awsdns-39.net.',
		'ns-1895.awsdns-44.co.uk.',
		'ns-200.awsdns-25.com.',
		'ns-1422.awsdns-49.org.',
	],
)
record_sets.append(record_set)

for domain in CONFIG['public']['domain_names']:
	for type in ['A', 'AAAA']:
		record_set = troposphere.route53.RecordSet(
			Name=domain + '.',
			Type=type,
			AliasTarget=troposphere.route53.AliasTarget(
				HostedZoneId=CONFIG['target']['cloudfront_hosted_zone_id'],
				DNSName=CONFIG['target']['domain_name'] + '.',
			),
		)
		record_sets.append(record_set)

record_set_group = troposphere.route53.RecordSetGroup(
	'RecordSetGroup',
	template=template,
	HostedZoneId=troposphere.Ref(hosted_zone),
	RecordSets=record_sets,
)

print(template.to_json())
