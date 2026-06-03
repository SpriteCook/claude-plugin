---
name: spritecook-use-dual-grid-tilesets
description: "Implementation guide for using SpriteCook top-down 15-piece tilesets with a dual-grid autotile renderer. Use when explaining or coding how to map a 4x4 15-piece tileset image into terrain using SpriteCook's dual-grid mask system."
---

# SpriteCook Dual-Grid 15-Piece Tilesets

Use this skill when implementing a top-down 15-piece SpriteCook tileset in a game engine or custom renderer.

This skill is about using a generated tileset. For generation, use `spritecook-generate-tilesets`.

## Concept

A dual-grid tileset stores terrain as logical painted cells, then renders visible tiles between those cells. Each rendered tile is chosen from the four logical cells around it.

For each rendered tile, sample:

- top-left logical cell
- top-right logical cell
- bottom-left logical cell
- bottom-right logical cell

That four-cell pattern becomes a 4-bit mask. The mask chooses one frame from the 4x4 15-piece atlas.

## Mask Order

Use SpriteCook's current mask bit order:

```ts
let mask = 0
if (filled(x - 1, y - 1)) mask |= 1 // top-left
if (filled(x,     y - 1)) mask |= 2 // top-right
if (filled(x - 1, y    )) mask |= 4 // bottom-left
if (filled(x,     y    )) mask |= 8 // bottom-right
```

Mask `0` renders nothing. Other masks map into the 4x4 atlas through this lookup:

```ts
const frameByMask = [
  -1,
  15,
  8,
  9,
  0,
  11,
  14,
  7,
  13,
  4,
  1,
  10,
  3,
  2,
  5,
  6,
]
```

The atlas cell is:

```ts
const frame = frameByMask[mask]
if (frame < 0) return null
const atlasColumn = frame % 4
const atlasRow = Math.floor(frame / 4)
```

## Renderer Pseudocode

```ts
type CellMap = boolean[] // width * height logical terrain cells

function cellIndex(x: number, y: number, columns: number) {
  return y * columns + x
}

function isFilled(cells: CellMap, x: number, y: number, columns: number, rows: number) {
  return x >= 0 && y >= 0 && x < columns && y < rows && cells[cellIndex(x, y, columns)] === true
}

function dualGridMask(cells: CellMap, x: number, y: number, columns: number, rows: number) {
  let mask = 0
  if (isFilled(cells, x - 1, y - 1, columns, rows)) mask |= 1
  if (isFilled(cells, x,     y - 1, columns, rows)) mask |= 2
  if (isFilled(cells, x - 1, y,     columns, rows)) mask |= 4
  if (isFilled(cells, x,     y,     columns, rows)) mask |= 8
  return mask
}

function atlasCellForMask(mask: number) {
  const frameByMask = [-1, 15, 8, 9, 0, 11, 14, 7, 13, 4, 1, 10, 3, 2, 5, 6]
  const frame = frameByMask[Math.max(0, Math.min(15, Math.floor(mask)))]
  if (frame < 0) return null
  return { column: frame % 4, row: Math.floor(frame / 4) }
}

function renderDualGrid(ctx, atlasImage, cells: CellMap, columns: number, rows: number, tileSize: number) {
  for (let y = 0; y <= rows; y += 1) {
    for (let x = 0; x <= columns; x += 1) {
      const mask = dualGridMask(cells, x, y, columns, rows)
      const atlasCell = atlasCellForMask(mask)
      if (!atlasCell) continue

      ctx.drawImage(
        atlasImage,
        atlasCell.column * tileSize,
        atlasCell.row * tileSize,
        tileSize,
        tileSize,
        x * tileSize,
        y * tileSize,
        tileSize,
        tileSize,
      )
    }
  }
}
```

## Practical Notes

- Render one more tile column and row than the logical map size because rendered tiles sit around painted logical cells.
- For pixel art, disable smoothing and use nearest-neighbor scaling.
- Treat mask `15` as the filled interior tile and mask `0` as transparent/no draw.
- Use the generated atlas exactly as a 4x4 grid of equal tile-sized cells.
- Do not reinterpret the sheet as a normal 8-neighbor blob tileset; this mapping is specifically SpriteCook's dual-grid 15-piece layout.
