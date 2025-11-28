"""
PostgreSQL Backup and Sync Script
Inspired by SortDesk's postgresql-backup-sync pattern
Automates PostgreSQL backups with cloud sync support
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
from typing import Optional
import gzip
import shutil

try:
    import boto3
    from botocore.exceptions import ClientError
    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False

try:
    from azure.storage.blob import BlobServiceClient
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

from loguru import logger


class PostgreSQLBackup:
    """PostgreSQL backup automation with cloud sync"""
    
    def __init__(
        self,
        db_host: str,
        db_name: str,
        db_user: str,
        db_password: Optional[str] = None,
        backup_dir: str = "/backup",
        files_to_keep: int = 7,
        compress: bool = True
    ):
        self.db_host = db_host
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password or os.getenv('POSTGRES_PASSWORD', '')
        self.backup_dir = Path(backup_dir)
        self.files_to_keep = files_to_keep
        self.compress = compress
        
        # Cloud storage configuration
        self.aws_bucket = os.getenv('AWS_BUCKET_NAME')
        self.aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_region = os.getenv('AWS_REGION', 'us-east-1')
        
        self.azure_connection_str = os.getenv('AZ_CONNECTION_STR')
        self.azure_container = os.getenv('AZ_CONTAINER_NAME')
        
        # Ensure backup directory exists
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        logger.add(
            self.backup_dir / "backup.log",
            rotation="1 day",
            retention="30 days",
            level="INFO"
        )
    
    def create_backup(self) -> Path:
        """
        Create PostgreSQL backup
        
        Returns:
            Path to backup file
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"{self.db_name}_{timestamp}.sql"
        backup_path = self.backup_dir / backup_filename
        
        logger.info(f"Creating backup: {backup_filename}")
        
        # Set PGPASSWORD environment variable
        env = os.environ.copy()
        if self.db_password:
            env['PGPASSWORD'] = self.db_password
        
        # Build pg_dump command
        cmd = [
            'pg_dump',
            '-h', self.db_host,
            '-U', self.db_user,
            '-d', self.db_name,
            '-F', 'p',  # Plain SQL format
            '-f', str(backup_path)
        ]
        
        try:
            result = subprocess.run(
                cmd,
                env=env,
                capture_output=True,
                text=True,
                check=True
            )
            
            logger.info(f"Backup created successfully: {backup_path}")
            
            # Compress if requested
            if self.compress:
                compressed_path = self._compress_backup(backup_path)
                # Remove uncompressed file
                backup_path.unlink()
                backup_path = compressed_path
                logger.info(f"Backup compressed: {compressed_path}")
            
            return backup_path
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Backup failed: {e.stderr}")
            raise Exception(f"Backup failed: {e.stderr}")
    
    def _compress_backup(self, backup_path: Path) -> Path:
        """Compress backup file using gzip"""
        compressed_path = backup_path.with_suffix('.sql.gz')
        
        with open(backup_path, 'rb') as f_in:
            with gzip.open(compressed_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        return compressed_path
    
    def sync_to_aws(self, backup_path: Path) -> bool:
        """
        Sync backup to AWS S3
        
        Args:
            backup_path: Path to backup file
            
        Returns:
            True if successful
        """
        if not AWS_AVAILABLE:
            logger.warning("boto3 not available. AWS sync skipped.")
            return False
        
        if not self.aws_bucket or not self.aws_access_key or not self.aws_secret_key:
            logger.warning("AWS credentials not configured. AWS sync skipped.")
            return False
        
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.aws_region
            )
            
            # Upload to S3
            s3_key = f"backups/{backup_path.name}"
            s3_client.upload_file(
                str(backup_path),
                self.aws_bucket,
                s3_key
            )
            
            logger.info(f"Backup synced to S3: s3://{self.aws_bucket}/{s3_key}")
            return True
            
        except ClientError as e:
            logger.error(f"AWS sync failed: {e}")
            return False
    
    def sync_to_azure(self, backup_path: Path) -> bool:
        """
        Sync backup to Azure Blob Storage
        
        Args:
            backup_path: Path to backup file
            
        Returns:
            True if successful
        """
        if not AZURE_AVAILABLE:
            logger.warning("azure-storage-blob not available. Azure sync skipped.")
            return False
        
        if not self.azure_connection_str or not self.azure_container:
            logger.warning("Azure credentials not configured. Azure sync skipped.")
            return False
        
        try:
            blob_service_client = BlobServiceClient.from_connection_string(
                self.azure_connection_str
            )
            
            blob_client = blob_service_client.get_blob_client(
                container=self.azure_container,
                blob=f"backups/{backup_path.name}"
            )
            
            with open(backup_path, 'rb') as data:
                blob_client.upload_blob(data, overwrite=True)
            
            logger.info(f"Backup synced to Azure: {self.azure_container}/backups/{backup_path.name}")
            return True
            
        except Exception as e:
            logger.error(f"Azure sync failed: {e}")
            return False
    
    def sync_to_bunnycdn(self, backup_path: Path) -> bool:
        """
        Sync backup to BunnyCDN
        
        Args:
            backup_path: Path to backup file
            
        Returns:
            True if successful
        """
        bunny_storage = os.getenv('BUNNY_STORAGE_ZONE')
        bunny_key = os.getenv('BUNNY_ACCESS_KEY')
        bunny_hostname = os.getenv('BUNNY_CDN_HOSTNAME', 'storage.bunnycdn.com')
        
        if not bunny_storage or not bunny_key:
            logger.warning("BunnyCDN credentials not configured. BunnyCDN sync skipped.")
            return False
        
        try:
            import requests
            
            url = f"https://{bunny_hostname}/{bunny_storage}/backups/{backup_path.name}"
            headers = {
                'AccessKey': bunny_key
            }
            
            with open(backup_path, 'rb') as f:
                response = requests.put(url, data=f, headers=headers, timeout=300)
            
            if response.status_code in (200, 201):
                logger.info(f"Backup synced to BunnyCDN: {url}")
                return True
            else:
                logger.error(f"BunnyCDN sync failed: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"BunnyCDN sync failed: {e}")
            return False
    
    def cleanup_old_backups(self):
        """Remove old backups keeping only the most recent N files"""
        backup_files = sorted(
            self.backup_dir.glob(f"{self.db_name}_*.sql*"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        if len(backup_files) > self.files_to_keep:
            files_to_delete = backup_files[self.files_to_keep:]
            for file_path in files_to_delete:
                logger.info(f"Removing old backup: {file_path.name}")
                file_path.unlink()
    
    def run_backup(self, sync_to_cloud: bool = True):
        """
        Run complete backup process
        
        Args:
            sync_to_cloud: Whether to sync to cloud storage
        """
        try:
            # Create backup
            backup_path = self.create_backup()
            
            # Sync to cloud
            if sync_to_cloud:
                self.sync_to_aws(backup_path)
                self.sync_to_azure(backup_path)
                self.sync_to_bunnycdn(backup_path)
            
            # Cleanup old backups
            self.cleanup_old_backups()
            
            logger.info("Backup process completed successfully")
            
        except Exception as e:
            logger.error(f"Backup process failed: {e}")
            raise


def main():
    """Main entry point for backup script"""
    parser = argparse.ArgumentParser(description='PostgreSQL Backup and Sync')
    parser.add_argument('--host', default=os.getenv('POSTGRES_HOST', 'localhost'))
    parser.add_argument('--database', default=os.getenv('POSTGRES_DB', 'sketch2bim'))
    parser.add_argument('--user', default=os.getenv('POSTGRES_USER', 'postgres'))
    parser.add_argument('--password', default=os.getenv('POSTGRES_PASSWORD'))
    parser.add_argument('--backup-dir', default=os.getenv('BACKUP_DIR', '/backup'))
    parser.add_argument('--files-to-keep', type=int, default=int(os.getenv('FILES_TO_KEEP', '7')))
    parser.add_argument('--no-compress', action='store_true')
    parser.add_argument('--no-cloud-sync', action='store_true')
    
    args = parser.parse_args()
    
    backup = PostgreSQLBackup(
        db_host=args.host,
        db_name=args.database,
        db_user=args.user,
        db_password=args.password,
        backup_dir=args.backup_dir,
        files_to_keep=args.files_to_keep,
        compress=not args.no_compress
    )
    
    backup.run_backup(sync_to_cloud=not args.no_cloud_sync)


if __name__ == '__main__':
    main()

