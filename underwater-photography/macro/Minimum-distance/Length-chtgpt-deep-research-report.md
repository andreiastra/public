# Executive Summary  
For the OM SYSTEM OM-1 Mark II with Olympus M.Zuiko 60 mm f/2.8 Macro (1× magnification), the *dry* minimum focus is 0.19 m from the sensor【24†L460-L462】 (≈7.5″) yielding about 0.10 m from the lens front.  This gives 1× magnification (1:1).  In a Nauticam NA‑OM1 housing with a flat macro port (optical glass, n≈1.52【16†L747-L752】, water n=1.333), the *underwater* focus distance becomes about **0.253 m** (sensor to subject), and the subject to front‐of‐port distance ≈0.253 m.  The flat port produces a virtual image closer to the lens, effectively “magnifying” the image by ≈25–28%【36†L137-L140】【36†L231-L235】.  Thus underwater the system still achieves roughly **1×–1.3×** reproduction (about +28% size), with focus markers shifted accordingly.  Using a dome port (water-to-glass curvature matched to lens) largely eliminates this refraction: focus distance remains ~0.19 m and working distance ~0.10 m (i.e. similar to dry), with no extra magnification【36†L231-L235】【36†L196-L200】.  Adding Nauticam extension rings (MP45+20 or MP35+30) simply increases the lens-to-port spacing by 20–30 mm, lengthening both dry and wet focus distances by that amount.  The tables below summarize these values under assumed n_water=1.333 and n_port=1.52. 

【67†embed_image】 *Figure: Underwater macro subject (pink coral, M.Zuiko 60 mm) – illustrating close working distances in macro shooting (OM-1 II & Nauticam housing).*

## Dry (Air) Focusing and Working Distances  
- **Sensor‐to‐subject focus** = 0.19 m (min)【24†L460-L462】.  With the OM‐system flange (≈19.25 mm) and lens extending ~80 mm beyond the mount【69†L301-L304】【70†L0-L4】, this implies about 0.10 m from the *front element* to the subject (working distance).  In fact, Olympus specifies “roughly 10 cm” from the front element at 1:1【70†L0-L4】.  
- **Magnification** M_dry = 1× at this setting (by design of the macro lens).  (Lens formula 1/f=1/so+1/si and M=si/so with the effective focal length arranged so that M=1 at so=0.19 m.)  
- **Definition:** Working distance (WD_dry) is taken as subject‑to‑*front of lens*.  

<table>
<thead><tr><th>Scenario</th><th>Sensor–Subject<br>(dry focus)</th><th>Subject–LensFront<br>(WD<sub>dry</sub>)</th><th>Magnification</th></tr></thead>
<tbody>
<tr><td>OM‑1 II + M.Zuiko 60 mm in air</td><td>0.190 m【24†L460-L462】</td><td>≈0.100 m (≈10 cm)【70†L0-L4】</td><td>1.00× (1:1)</td></tr>
</tbody>
</table>

## Nauticam NA‑OM1 Housing and Ports  
- **Housing:** Nauticam NA‑OM1 (for OM-1/II) uses the N85 port system.  It can accept flat *Macro Port 65* for the 60 mm lens【11†L266-L274】 (optical-glass, 100 m depth【16†L742-L750】), or smaller flat ports with extension rings (MP45+Ext20 or MP35+Ext30)【11†L266-L274】.  
- **Flat Port Material:** Optical glass (n≈1.50–1.52)【16†L747-L752】.  
- **Dome Port:** Nauticam dome ports (not usually paired with a macro prime) effectively behave as if the lens were still “in air” for refraction – eliminating the flat‐port virtual image.  (We include dome for comparison.)  
- **Extension Rings:** Adding an extension ring (20 mm or 30 mm) simply shifts the lens farther from the port by that length.  

## Underwater Focus and Working Distances (Flat Port)  
A flat port creates a **virtual image** of an underwater object closer to the lens【32†L150-L158】.  In effect, an object at distance _d_ in water appears at _d/n_ in air terms.  Thus:  

- Let _S<sub>air</sub>_ = 0.190 m (dry focus from sensor).  In water (n=1.333), the required object distance _S<sub>water</sub>_ satisfies _S<sub>air</sub>_ = _S<sub>water</sub>_/1.333.  Solving gives **S<sub>water</sub> ≈0.253 m**.  This is the new sensor-to-subject distance underwater.  
- **Underwater WD<sub>port</sub>:** Since we define WD as subject-to-port-front, and we assume the subject is just outside the port, WD_port ≈ 0.253 m as well.  (If we accounted for port thickness _t_ and an internal air gap, it would be WD_port = S<sub>water</sub> + t + gap – but here t is small relative.)  
- **Underwater WD<sub>lens</sub>:** The subject is 0.253 m from the port; the lens front is closer (inside housing).  In practice, WD_lens_under ≈ WD_dry × 1.333 ≈ 0.100×1.333 = 0.133 m.  
- **Magnification (flat port):** The flat port effectively increases magnification by about 25–28%【36†L137-L140】【36†L231-L235】 (objects appear closer).  Thus M_water ≈1.28× the dry M.  Since M_dry=1.00×, we get **M_water ≈1.28×**.  (Equivalently, the image covers a 28% larger angle of view underwater for the same lens setting.)  

These results are summarized in the table below (flat vs. dome vs. extension cases):

<table>
<thead><tr><th>Configuration</th><th>Assumptions</th><th>Sensor–Subject</th><th>Subject–Port Front</th><th>WD (Lens Front)</th><th>Effective M</th></tr></thead>
<tbody>
<tr><td>Dry (air)</td><td> n_air=1.000</td><td>0.190 m【24†L460-L462】</td><td>–</td><td>≈0.100 m【70†L0-L4】</td><td>1.00×</td></tr>
<tr><td>Underwater, Flat Port</td><td> n_water=1.333, n_port≈1.52</td><td>≈0.253 m (×1.333)</td><td>≈0.253 m (port surface)</td><td>≈0.133 m (≈0.100×1.333)</td><td>~1.28×【36†L137-L140】【36†L231-L235】</td></tr>
<tr><td>Underwater, Dome Port</td><td> n_effective≈1.000</td><td>≈0.190 m</td><td>≈0.190 m</td><td>≈0.100 m</td><td>≈1.00× (no extra mag)【36†L196-L200】</td></tr>
<tr><td>Flat Port + Ext 20 mm</td><td>Lens 20 mm farther</td><td>≈0.210 m</td><td>≈0.210 m</td><td>≈0.120 m</td><td>≈1.28×</td></tr>
<tr><td>Flat Port + Ext 30 mm</td><td>Lens 30 mm farther</td><td>≈0.220 m</td><td>≈0.220 m</td><td>≈0.121 m</td><td>≈1.28×</td></tr>
</tbody>
</table>

- *Notes:* The “Flat Port + Ext” lines are estimated by simply adding 20 mm or 30 mm to the dry focus (0.19 m) before applying the n=1.333 factor.  WD (Lens Front) is similarly scaled.  Exact values depend on the housing’s internal layout.  All magnifications assume the port remains flat (so the 1.28× boost still applies).

## Calculation Details  

1. **Dry Minimum Focus (Air):** From Olympus/OM System specs, the 60 mm macro’s closest focus is 0.19 m【24†L460-L462】 from the *sensor plane*.  Subtracting the M4/3 flange distance (~19.25 mm) and lens length (~80 mm to front element) yields ~0.10 m from the *front element*【70†L0-L4】.  

2. **Lens Formula (Air):** For completeness, a thin-lens approximation (effective focal f_eff≈95 mm to yield 1:1 at 0.19 m) gives 1/f_eff = 1/so + 1/si with so=190 mm, producing M=si/so=1.0.  (In reality, complex multi-element optics, but the result is 1×.)  

3. **Refractive Effects (Flat Port):** Underwater, light from a point at real distance S_water in water appears to originate from a *virtual object* distance S_air = S_water/1.333 in air【32†L150-L158】.  To focus at M=1, we need S_air (virtual) = 0.19 m (dry).  Thus S_water ≈0.19×1.333 = 0.253 m.  This means the camera must now be about 25.3 cm from the subject (measured at the port).  

4. **Working Distance (Flat Port):** In air, subject-to-lens-front = ~0.10 m.  Underwater, that distance (in the medium of water) is effectively larger: WD_under ≈WD_air×1.333 ≈0.133 m.  But if we measure to the port face, WD_port ≈0.253 m.  

5. **Focus Shift Correction:** The lens’ focus scale (marked for air) no longer applies underwater.  One must refocus about 33% further out.  In practice, Nauticam and Olympus note that focus marks are “wrong” underwater【36†L231-L235】【32†L150-L158】.  (Some call this the “wet focus shift.”)  No lens elements move involuntarily – it’s just geometric.  

6. **Magnification Change:** Flat ports “magnify” images.  The GDome tutorial explains this arises because objects “appear closer… making them look bigger”【32†L150-L158】.  Empirically, a flat port increases image size ~25–28%【36†L137-L140】.  Thus M_water ≈1×1.28.  Dome ports have the opposite effect: they preserve angular size, so M≈1 (no boost)【36†L231-L235】【36†L196-L200】.  

7. **Extension Rings:** A 20 mm extender increases all distances by 0.02 m.  So dry focus becomes ~0.21 m, underwater ~0.28 m.  Magnification is slightly reduced by the longer extension, but the flat port’s ~28% boost still applies.  (We omit detailed focus formula adjustments because precise housing distances are proprietary.)  

Below is a **calculation flowchart** summarizing these steps:  

```mermaid
flowchart LR
    A[Input: Dry Focus 0.190 m (sensor)] --> B[Compute WD<sub>dry</sub> ≈0.100 m (front)] 
    A --> C[Flat Port Underwater: S<sub>water</sub> = 0.190×1.333 = 0.253 m]
    C --> D[WD<sub>port</sub> ≈0.253 m (flat port surface)]
    C --> E[WD<sub>lens</sub> = 0.100×1.333 ≈0.133 m]
    E --> F[Compute M_air=1×; M_under ≈M_air×1.28 (≈1.28×)【36†L137-L140】]
    subgraph FlatPort
      C
      D
      E
      F
    end
    B --> G[Dome Port Underwater: S_water ~0.190 m (no refraction)]
    G --> H[WD_port≈0.190 m; M≈1.0 (no mag)【36†L196-L200】]
```

*Mermaid flowchart: Calculating focus/WD in air and water (flat vs. dome ports).*  

## Sources and Notes  
- **Camera/Lens Specs:** OM-1 II tech specs and Olympus literature list the 60 mm Macro’s closest focus as 0.19 m【24†L460-L462】.  Photographic review confirms 1:1 at 19 cm【69†L259-L263】 and notes subjects ~10 cm from front at 1:1【70†L0-L4】.  
- **Nauticam Ports:** Official Nauticam documentation describes Macro Port 65 (optical glass) for this lens【11†L266-L274】【16†L747-L752】.  GDome and Oceanity explain flat‑port optics【32†L150-L158】【36†L137-L140】.  
- **Refractive Indices:** We used n_water=1.333 (pure water) and n_glass≈1.52 (typical crown glass).  Results are approximate; real ports have finite thickness.  
- **Calculations:** Steps use standard refraction (virtual image) and thin-lens approximations.  If any official spec (e.g. port thickness) was unavailable, we stated assumptions.  All key values are in the tables and flowchart.  

**References:** Official specs and port info【24†L460-L462】【16†L747-L752】, Nauticam announcements【11†L266-L274】, and optical theory sources【32†L150-L158】【36†L137-L140】.