// Optimise les visuels de la visite d'accueil (générés avec Higgsfield).
// Les PNG sources pèsent ~5 Mo chacun : ils restent hors du dépôt.
//
// Usage : node scripts/build_journey_images.mjs <dossier-source>
// Le dossier contient d0.png..d7.png (16:9) et m0.png..m7.png (9:16), dans
// l'ordre des lieux de src/components/PlacesJourney.astro.
//
// Les boucles vidéo du portrait (public/videos/journey) sont réencodées à part,
// sans piste son et avec l'index en tête pour démarrer avant la fin du
// téléchargement :
//   ffmpeg -i in.mp4 -an -c:v libx264 -preset slow -crf 25 -pix_fmt yuv420p -movflags +faststart out.mp4
import sharp from 'sharp';
import { mkdir } from 'node:fs/promises';
import path from 'node:path';

const SLUGS = [
  'lome-hq',
  'software-studio',
  'saas-ops',
  'creative-studio',
  'port-lome',
  'logistics-warehouse',
  'it-showroom',
  'founder',
];

const source = process.argv[2];
if (!source) {
  console.error('Usage : node scripts/build_journey_images.mjs <dossier-source>');
  process.exit(1);
}

const out = path.resolve('public/images/journey');
await mkdir(out, { recursive: true });

for (const [i, slug] of SLUGS.entries()) {
  const jobs = [
    ...[1280, 1920, 2560].map((w) => [`d${i}.png`, w, `${slug}-${w}.webp`]),
    ...[900, 1300].map((w) => [`m${i}.png`, w, `${slug}-m${w}.webp`]),
  ];
  for (const [file, width, name] of jobs) {
    const info = await sharp(path.join(source, file))
      .resize({ width, withoutEnlargement: true })
      .webp({ quality: width >= 1920 ? 72 : 76, effort: 6 })
      .toFile(path.join(out, name));
    console.log(`${name}  ${Math.round(info.size / 1024)} Ko`);
  }
}
