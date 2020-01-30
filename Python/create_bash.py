

with open('/home/mcarruth/Downloads/out.txt') as fin:
    lines = fin.readlines()

lines = lines[2:-2]

cmds = []
cleanup = []
for line in lines:
    a = line.split('|')
    old_location = f's3://{a[3].strip()}/{a[4].strip()}'
    new_location = f's3://{a[3].strip()}/image_telemetry.{a[2].strip()}.{a[0].strip()}.{a[1].strip()}.json'
    cmds.append(f'aws s3 cp {old_location} {new_location};\n')
    cleanup.append(f'aws s3 rm {old_location};\n')
with open('/home/mcarruth/Downloads/aws.sh', 'w+') as f:
    f.writelines(cmds)

with open('/home/mcarruth/Downloads/aws_rm.sh', 'w+') as f:
    f.writelines(cleanup)

with open('/home/mcarruth/Downloads/psql.sh', 'w+') as f:
    f.write('BEGIN; UPDATE image_slot SET s3_bucket="bsg-gemini-prod-files", s3_key=SUBSTRING(s3_key, 0, LENGTH(s3_key)-15) WHERE s3_bucket LIKE "%sfx-packets"; ROLLBACK;')
