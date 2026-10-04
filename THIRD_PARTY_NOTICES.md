# Third-party provenance and notices

## LZX decoder

`src/stardew/infrastructure/xnb/lzx.py` ports MonoGame's LzxDecoder.cs and selects
the Microsoft Public License option of its LGPL 2.1 / MS-PL dual license.
Canonical Huffman decoding replaces the original lookup-table optimization.
The XNB frame reader follows MonoGame Foundation's LzxDecoderStream.

Sources retrieved on 2026-09-12:
- https://raw.githubusercontent.com/MonoGame/MonoGame/develop/MonoGame.Framework/Content/LzxDecoder.cs
- https://raw.githubusercontent.com/MonoGame/MonoGame/develop/MonoGame.Framework/Utilities/LzxStream/LzxDecoderStream.cs

Original decoder header (all copyright and license notices retained):

```text
#region HEADER
/* This file was derived from libmspack
 * (C) 2003-2004 Stuart Caie.
 * (C) 2011 Ali Scissons.
 *
 * The LZX method was created by Jonathan Forbes and Tomi Poutanen, adapted
 * by Microsoft Corporation.
 *
 * This source file is Dual licensed; meaning the end-user of this source file
 * may redistribute/modify it under the LGPL 2.1 or MS-PL licenses.
 */
#region LGPL License
/* GNU LESSER GENERAL PUBLIC LICENSE version 2.1
 * LzxDecoder is free software; you can redistribute it and/or modify it under
 * the terms of the GNU Lesser General Public License (LGPL) version 2.1
 */
#endregion
#region MS-PL License
/*
 * MICROSOFT PUBLIC LICENSE
 * This source code is subject to the terms of the Microsoft Public License (Ms-PL).
 *
 * Redistribution and use in source and binary forms, with or without modification,
 * is permitted provided that redistributions of the source code retain the above
 * copyright notices and this file header.
 *
 * Additional copyright notices should be appended to the list above.
 *
 * For details, see <http://www.opensource.org/licenses/ms-pl.html>.
 */
#endregion
/*
 * This derived work is recognized by Stuart Caie and is authorized to adapt
 * any changes made to lzxd.c in his libmspack library and will still retain
 * this dual licensing scheme. Big thanks to Stuart Caie!
 *
 * DETAILS
 * This file is a pure C# port of the lzxd.c file from libmspack, with minor
 * changes towards the decompression of XNB files. The original decompression
 * software of LZX encoded data was written by Suart Caie in his
 * libmspack/cabextract projects, which can be located at
 * http://http://www.cabextract.org.uk/
 */
#endregion


```

## MonoGame license

﻿Microsoft Public License (Ms-PL)
MonoGame - Copyright © 2009-2026 MonoGame Foundation, Inc

All rights reserved.

This license governs use of the accompanying software. If you use the software,
you accept this license. If you do not accept the license, do not use the
software.

1. Definitions

The terms "reproduce," "reproduction," "derivative works," and "distribution"
have the same meaning here as under U.S. copyright law.

A "contribution" is the original software, or any additions or changes to the
software.

A "contributor" is any person that distributes its contribution under this
license.

"Licensed patents" are a contributor's patent claims that read directly on its
contribution.

2. Grant of Rights

(A) Copyright Grant- Subject to the terms of this license, including the
license conditions and limitations in section 3, each contributor grants you a
non-exclusive, worldwide, royalty-free copyright license to reproduce its
contribution, prepare derivative works of its contribution, and distribute its
contribution or any derivative works that you create.

(B) Patent Grant- Subject to the terms of this license, including the license
conditions and limitations in section 3, each contributor grants you a
non-exclusive, worldwide, royalty-free license under its licensed patents to
make, have made, use, sell, offer for sale, import, and/or otherwise dispose of
its contribution in the software or derivative works of the contribution in the
software.

3. Conditions and Limitations

(A) No Trademark License- This license does not grant you rights to use any
contributors' name, logo, or trademarks.

(B) If you bring a patent claim against any contributor over patents that you
claim are infringed by the software, your patent license from such contributor
to the software ends automatically.

(C) If you distribute any portion of the software, you must retain all
copyright, patent, trademark, and attribution notices that are present in the
software.

(D) If you distribute any portion of the software in source code form, you may
do so only under this license by including a complete copy of this license with
your distribution. If you distribute any portion of the software in compiled or
object code form, you may only do so under a license that complies with this
license.

(E) The software is licensed "as-is." You bear the risk of using it. The
contributors give no express warranties, guarantees or conditions. You may have
additional consumer rights under your local laws which this license cannot
change. To the extent permitted under your local laws, the contributors exclude
the implied warranties of merchantability, fitness for a particular purpose and
non-infringement.

-------------------------------------------------------------------------------

The MIT License (MIT)
Portions Copyright © The Mono.Xna Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.


## Existing predictor and game data

Geometry, map data and bubble rules are adapted from the existing MapPredictor
extraction. See src/stardew/resources/maps.provenance.json. This migration does not assert a new
upstream license over those materials. Artifact rules preserve the existing
inspection of installed Stardew Valley 1.6.15. The explicit schemas describe
serialization order and types inspected in StardewValley.GameData 1.6.15.24356.
Local game tables and personal saves are not distributed in Git.


## Plotting assets and format references

The bundled src/stardew/resources/fonts/DejaVuSans.ttf is DejaVu Sans, copyright
Bitstream, Inc. and the DejaVu contributors. Its full license is bundled at
src/stardew/resources/fonts/LICENSE.txt. It is used to render Unicode labels
consistently without depending on operating-system fonts.

The graphics reader interprets the tBIN10 wire format inspected in the installed
xTile reader and MonoGame Texture2D content layout. No game artwork or game
assemblies are bundled. Map and texture assets are read from the user's game
installation only when plotting is requested.
