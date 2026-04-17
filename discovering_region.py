import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, ClientError


def get_s3_client(region=None):
    try:
        # fallback padrão
        if not region:
            region = "us-east-1"

        return boto3.client("s3", region_name=region)

    except Exception as e:
        print(f"[ERRO] Falha ao criar cliente S3: {e}")
        return None


def list_buckets():
    print("\n📦 Listando buckets...")
    try:
        s3 = get_s3_client()
        response = s3.list_buckets()

        buckets = response.get("Buckets", [])
        if not buckets:
            print("Nenhum bucket encontrado.")
            return []

        for b in buckets:
            print(f" - {b['Name']}")

        return [b["Name"] for b in buckets]

    except NoCredentialsError:
        print("[ERRO] Credenciais não encontradas. Execute 'aws configure'.")
    except PartialCredentialsError:
        print("[ERRO] Credenciais incompletas.")
    except ClientError as e:
        print(f"[ERRO] AWS: {e}")
    except Exception as e:
        print(f"[ERRO] Inesperado: {e}")

    return []


def get_bucket_region(bucket_name):
    print(f"\n🌎 Descobrindo região do bucket: {bucket_name}")
    try:
        s3 = get_s3_client()
        response = s3.get_bucket_location(Bucket=bucket_name)

        region = response.get("LocationConstraint")

        # Regra da AWS: None = us-east-1
        if region is None:
            region = "us-east-1"

        print(f"Região: {region}")
        return region

    except ClientError as e:
        code = e.response["Error"]["Code"]

        if code == "NoSuchBucket":
            print("[ERRO] Bucket não existe.")
        elif code == "AccessDenied":
            print("[ERRO] Sem permissão para acessar o bucket.")
        else:
            print(f"[ERRO] AWS: {e}")

    except Exception as e:
        print(f"[ERRO] Inesperado: {e}")

    return None


def list_objects(bucket_name):
    print(f"\n📂 Listando objetos do bucket: {bucket_name}")

    region = get_bucket_region(bucket_name)
    if not region:
        print("Não foi possível determinar a região.")
        return

    try:
        s3 = get_s3_client(region)
        response = s3.list_objects_v2(Bucket=bucket_name)

        contents = response.get("Contents", [])

        if not contents:
            print("Bucket vazio ou sem permissão.")
            return

        for obj in contents:
            print(f" - {obj['Key']}")

    except ClientError as e:
        code = e.response["Error"]["Code"]

        if code == "AccessDenied":
            print("[ERRO] Sem permissão para listar objetos.")
        elif code == "NoSuchBucket":
            print("[ERRO] Bucket não existe.")
        else:
            print(f"[ERRO] AWS: {e}")

    except Exception as e:
        print(f"[ERRO] Inesperado: {e}")


def main():
    # 1. Listar buckets da conta
    buckets = list_buckets()

    # 2. Se quiser testar manualmente um bucket específico:
    bucket_name = "movida-dump-semparar"

    # 3. Descobrir região + listar objetos
    list_objects(bucket_name)


if __name__ == "__main__":
    main()