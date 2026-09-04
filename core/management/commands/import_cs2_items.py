import json
import os
from pathlib import Path
from urllib.parse import urlparse

import requests
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand

from core.models import Case, Skin   # change if needed


class Command(BaseCommand):
    help = "Import CS2 cases & skins and download their images"

    def handle(self, *args, **options):
        data_dir = Path(__file__).resolve().parent.parent.parent / "data"

        # Because crates.json and skins.json are folders
        crates_file = data_dir / "crates.json" / "crates.json"
        skins_file = data_dir / "skins.json" / "skins.json"

        # Fallback: try to find any .json file inside the folders
        if not crates_file.exists():
            possible = list((data_dir / "crates.json").glob("*.json"))
            crates_file = possible[0] if possible else None

        if not skins_file.exists():
            possible = list((data_dir / "skins.json").glob("*.json"))
            skins_file = possible[0] if possible else None

        if not crates_file or not skins_file:
            self.stdout.write(self.style.ERROR("Could not find the real JSON files"))
            self.stdout.write(f"Checked in: {data_dir}")
            return

        self.stdout.write(f"Using crates file: {crates_file}")
        self.stdout.write(f"Using skins file:  {skins_file}")

        # ---------- Import Cases ----------
        with open(crates_file, encoding="utf-8") as f:
            crates = json.load(f)

        self.stdout.write("Importing cases...")
        for crate in crates:
            if crate.get("type") != "Case":
                continue

            case, created = Case.objects.update_or_create(
                name=crate["name"],
                defaults={"image_url": crate.get("image", "")},
            )

            if case.image_url and not case.image:
                self.download_image(case, case.image_url, "cases")

        # ---------- Import Skins ----------
        with open(skins_file, encoding="utf-8") as f:
            skins = json.load(f)

        self.stdout.write("Importing skins...")
        for item in skins:
            skin, created = Skin.objects.update_or_create(
                name=item["name"],
                defaults={
                    "weapon": item.get("weapon", {}).get("name", ""),
                    "rarity": item.get("rarity", {}).get("name", ""),
                    "image_url": item.get("image", ""),
                },
            )

            if skin.image_url and not skin.image:
                self.download_image(skin, skin.image_url, "skins")

        self.stdout.write(self.style.SUCCESS("Finished!"))

    def download_image(self, obj, url, folder):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()

            path = urlparse(url).path
            filename = os.path.basename(path)
            if not filename or "." not in filename:
                filename = f"{obj.pk}.png"

            obj.image.save(f"{folder}/{filename}", ContentFile(response.content), save=True)
            self.stdout.write(f"  ✓ {obj.name}")

        except Exception as e:
            self.stdout.write(self.style.WARNING(f"  ✗ Failed {obj.name}: {e}"))