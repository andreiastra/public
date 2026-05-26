# Custom Mode C2: Underwater Wide-Angle & Fisheye Guide

This document outlines the technical configuration and in-water strategy for transitioning from a macro setup to wide-angle/fisheye photography using the **OM SYSTEM OM-1 Mark II** and the **M.Zuiko 8mm f/1.8 Fisheye PRO** lens, paired with a single **Backscatter Hybrid Flash (HF-1)** and a dome diffuser.

---

## 1. Custom Mode 2 (C2) Camera Settings

Optimized for rapid deployment when shooting expansive seascapes, close-focus wide-angle (CFWA), or kelp forests.

### Primary Exposure & Drive
* **Shooting Mode:** **M (Manual)** – Crucial for independent management of ambient light and strobe power.
* **Aperture:** **f/8.0** – Default optical sweet spot for corner-to-corner sharpness behind a dome port. Drop to **f/5.6** only in extremely low light.
* **Shutter Speed:** **1/100s** – Baseline starting point to capture background color without sacrificing hand-held stability.
* **ISO:** **200** – Native base ISO for maximum dynamic range and lowest noise.
* **Drive Mode:** **Single Shot**
* **Image Stabilizer:** **S-IS AUTO** – Engages the camera's 5-axis body-side image stabilization.

### Autofocus Configuration
* **AF Mode:** **S-AF** (Switch to **C-AF** only for fast-moving pelagics or seals).
* **AF Target Mode:** **5-point Cross [X]** or **Small Zone (3x3)** – Prevents a single point from hunting in empty water; gives the system structural edges (reef walls, pier structures) to lock onto.
* **AF Limiter:** **OFF** – Allows the lens to utilize its entire range from the dome glass to infinity.
* **AF Illuminator:** **OFF** – Eliminates backscatter illumination right in front of the lens port.
* **AF-ON Button:** Mapped to **AF-ON** – Maintains back-button focus consistency with macro muscle memory.

### Flash & Trigger Integration
* **RC Mode:** **ON**
* **Flash Trigger Type:** **RC** (Via the OM Smart Control Flash Trigger).
* **HF-1 Mode Dial:** **SC (Smart Control)**
    * *Important:* Do **not** use the "SC Macro" profile. Standard **SC** utilizes the wide-angle TTL mapping optimized for the broad beam width.
* **HF-1 Target Light:** **Wide** or **Red** (High intensity helps AF contrast in low-light/dark water conditions).
* **Flash Sync Ceiling:** Hard locked at **1/250s** by system hardware limits.

---

## 2. Operational Ergonomics (Fn Lever Mapping)

Maintains physical consistency with your macro workflow but reassigns wide-angle priorities to the main positions.

| Fn Lever Position | Front Dial | Rear Dial |
| :--- | :--- | :--- |
| **Position 1** (Ambient & Depth) | **Aperture** (Controls foreground flash exposure & corner sharpness) | **Shutter Speed** (Controls background water brightness/color) |
| **Position 2** (Lighting & Sensitivity) | **Flash Exposure Compensation** (Fine-tunes strobe output/hot-spots) | **ISO** (Adjusts ambient light absorption in deep/dark water) |

---

## 3. Core Physics: The 1/60s Dual-Exposure Strategy

Dropping the shutter speed down to **1/60s, 1/80s, or 1/100s** is essential for wide-angle work because water absorbs natural light rapidly. A wide-angle frame operates as two separate exposures simultaneously:

1.  **The Foreground (Flash-Driven):** The burst duration of the HF-1 is extremely fast (**1/1000s to 1/5000s**). This ultra-fast burst completely freezes the motion of fish, kelp, or camera shake, ensuring tack-sharp foreground subjects regardless of shutter speed.
2.  **The Background (Ambient-Driven):** The remaining open time of the shutter window (the rest of the 1/60s) allows faint ambient sunlight to soak into the sensor. This transforms a flat, black background into a vibrant, glowing green or blue gradient that creates environmental depth.

### Mitigating Ghosting (Motion Blur)
* **The Risk:** Ghosting occurs only if ambient light hitting the foreground is strong enough to expose the subject by itself without a strobe.
* **The Reality in Irish Waters:** In typical coastal North Atlantic conditions, ambient light drops off sharply with depth. Your foreground subjects sit in relative darkness until hit by the strobe. Because there is insufficient natural light to create an ambient exposure stamp on the foreground at 1/60s, the image remains razor-sharp with no double-image effects.

---

## 4. Strobe Mechanics with the Dome Diffuser

The **Backscatter HF-1 Dome Diffuser** reshapes a standard directional strobe flash into a soft, wide-angle hemispherical beam covering up to $160^\circ$.

* **Exposure Penalty:** The hemisphere diffusion spreads light across a massive volume of water, resulting in a **0.5 to 1-stop drop in forward intensity**. The camera's RC TTL system will automatically increase flash output to compensate, but keep an eye on battery consumption and recycle times.
* **Warming Effect:** Dome diffusers slightly warm the light, which helps restore natural pinks, reds, and natural skin tones against cool green backgrounds.
* **Strobe Positioning Geometry:**
    * **Pull Arms Well Back:** Position the HF-1 **behind the handles of the housing**, well back from the plane of the dome port glass. Because light leaves the dome diffuser at extreme side angles, keeping the flash too far forward will illuminate the water column directly in front of the lens, causing blinding backscatter or lens flare.
    * **The "Toe-Out" Angle:** Point the strobe slightly *outward* (away from the center of the frame). Use the soft inner edge of the diffused light beam to paint the foreground subject, pushing illuminated particles away from the camera's line of sight.

---

## 5. In-Water Tuning Workflow

1.  **Read the Ambient Water:** Upon descending, ignore the strobes and evaluate the background water column in the viewfinder.
2.  **Brighten Dark/Muddy Backgrounds:** If the water looks black or dark gray-green, flip the Fn lever to **Position 1** and rotate the **Rear Dial** to drop the shutter speed down (**1/80s $\rightarrow$ 1/60s**) to open up the background ambient glow.
3.  **Darken Washed-out Scenery:** If the water column is losing contrast or overexposing, click the shutter speed up toward **1/160s or 1/200s**.
4.  **Manage Foreground Hotspots:** If the dome diffuser creates a hotspot on a close reef element, flip the Fn lever to **Position 2** and rotate the **Front Dial** to pull back the **Flash Exposure Compensation** to **-0.7 or -1.3** before adjusting the physical strobe arms.
