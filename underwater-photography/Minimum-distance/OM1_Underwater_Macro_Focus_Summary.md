# Comprehensive Optical and Physical Summary: OM-1 Mark II Underwater Macro Setup

This document consolidates and reconciles the technical specifications, physical boundaries, and optical behaviors of the OM SYSTEM OM-1 Mark II camera combined with the M.Zuiko Digital ED 60mm f/2.8 Macro lens inside the Nauticam NA-OM1 underwater housing. It integrates theoretical physics, manufacturer engineering specifications, and real-world testing dynamics.

---

## 1. System Components Profile

* **Camera Body:** OM SYSTEM OM-1 Mark II mirrorless camera featuring a 20MP stacked CMOS Micro Four Thirds (MFT) sensor ($13.0 \text{ mm} \times 17.3 \text{ mm}$ layout) and in-body image stabilization (IBIS) providing up to 7–8 EV of correction.
* **Optical Lens:** M.Zuiko Digital ED 60mm f/2.8 Macro lens (120mm full-frame equivalent). It employs a 13-element in 10-group configuration and a static inner focus system that maintains a constant lens barrel length of $82 \text{ mm}$ across all focus configurations.
* **Housing & Port System:** Nauticam NA-OM1 aluminum housing depth-rated to 100 meters, utilizing the N85 compact port interface. The primary configurations utilize either the dedicated flat **Macro Port 65** or a modular combination (Macro Port 45 with a Mini Extension Ring 20), both yielding an identical $79 \text{ mm}$ mechanical length.
* **Port Glass:** High-grade BK-7 optical glass featuring a nominal thickness of $8 \text{ mm}$, a diameter of $90 \text{ mm}$, and an external M67 thread interface for wet close-up optics.

---

## 2. Spatial & Focusing Boundaries (Air vs. Water)

The system's behavior changes dramatically depending on whether the external environment is air ($n_{\text{air}} \approx 1.00$) or seawater ($n_{\text{water}} \approx 1.333$). Light traveling from a subject through a flat port interface is governed by Snell's Law, altering apparent distances and magnification scales.

### Physical Distance Metrics Summary
The table below reconciles the spatial measurements of the setup across different mediums at the absolute mechanical minimum focus limit of the lens helical:

| Parameter / Metric | Land Specification (In-Air, No Housing) | Land Setup in Housing (Ruler Test Configuration) | Submerged Flat Port (Precise Optomechanical Model) | Submerged Dome Port (Refraction Mitigated) |
| :--- | :--- | :--- | :--- | :--- |
| **Refractive Index Baseline ($n$)** | $n = 1.000$ | $n_{\text{air}} = 1.000$, $n_{\text{glass}} \approx 1.52$ | $n_{\text{water}} = 1.333$, $n_{\text{glass}} \approx 1.52$ | $n_{\text{effective}} \approx 1.000$ |
| **Sensor-to-Subject Distance ($MFD$)** | **$19.0 \text{ cm}$ ($0.190 \text{ m}$)** | **$17.3 \text{ cm}$ ($0.173 \text{ m}$)** | **$22.0 \text{ cm}$ ($0.220 \text{ m}$)** | **$\approx 19.0 \text{ cm}$ ($0.190 \text{ m}$)** |
| **Working Distance: Port Front to Subject ($WD_{\text{port}}$)** | *N/A (No Housing Boundary)* | **$7.3 \text{ cm}$ ($0.073 \text{ m}$)** | **$12.0 \text{ cm}$ ($0.120 \text{ m}$)** | **$\approx 19.0 \text{ cm}$ *(Measured to glass apex)*** |
| **Working Distance: Lens Front to Subject ($WD_{\text{lens}}$)** | **$\approx 10.0 \text{ cm}$ ($0.100 \text{ m}$)** | **$\approx 8.1 \text{ cm}$ ($0.081 \text{ m}$)** | **$\approx 8.0 \text{ cm}$ ($0.080 \text{ m}$)** | **$\approx 10.0 \text{ cm}$ ($0.100 \text{ m}$)** |
| **Effective Magnification ($M$)** | $1.00\times$ (Native 1:1) | $1.00\times$ (Native 1:1) | **$1.33\times$** (Frame-Filling Boost) | $1.00\times$ (No added magnification) |
| **Sensor Frame Coverage ($H \times W$)** | $13.0 \text{ mm} \times 17.0 \text{ mm}$ | $13.0 \text{ mm} \times 17.0 \text{ mm}$ | **$9.8 \text{ mm} \times 12.8 \text{ mm}$** | $13.0 \text{ mm} \times 17.0 \text{ mm}$ |

---

## 3. Optical Core Concepts & Reconciliation

### The Split-Medium Track Length
A common point of confusion is why the submerged minimal focus distance ($MFD_{\text{wet}} = 22.0 \text{ cm}$) does not equal the simple multiplication of the native track length by the refractive index of water ($19.0 \text{ cm} \times 1.333 = 25.3 \text{ cm}$). 
* **The Reason:** The light path is split into two distinct mediums. Inside the pressurized Nauticam housing, a fixed **$10.0 \text{ cm}$ air chamber** exists from the camera sensor plane to the external surface of the port glass. 
* **The Math:** Refraction strictly acts upon the **wet segment** outside the housing. The native air working clearance from the port front to the subject is $9.0 \text{ cm}$ ($19.0 \text{ cm} \text{ MFD} - 10.0 \text{ cm} \text{ internal housing length} = 9.0 \text{ cm}$). When submerged, Snell's Law dictates that the true physical working distance required to form a virtual image matching the lens helix limit scales up: 
  $$WD_{\text{port (underwater)}} = MWD_{\text{land}} \times n_{\text{water}} = 9.0 \text{ cm} \times 1.333 = 11.97 \text{ cm} \approx 12.0 \text{ cm}$$
* Combining the internal dry segment ($10.0 \text{ cm}$) and external wet segment ($12.0 \text{ cm}$) yields the precise minimum focus distance of **$22.0 \text{ cm}$**.

### Glass-Induced Shortening in Air (The Ruler Test)
When conducting a dry test shot in air with the ruler extending directly from the front face of the Macro Port 65 to the subject, critical focus peaks at **$7.3 \text{ cm}$** instead of the theoretical unhoused $9.0 \text{ cm}$. 
* **The Reason:** This physical shortening is caused by the high refractive index of the $8 \text{ mm}$ thick BK-7 optical glass boundary ($n \approx 1.52$). 
* Even though the external medium is air, light traveling through the dense glass element undergoes minor positional refraction. This creates a small virtual image shift, tricking the lens internal optics into seeing the subject as if it were further away. Consequently, the entire mechanical housing assembly can move closer to the subject, reducing the external clearance to $7.3 \text{ cm}$ before hitting the physical focus helical limit.

### Magnification Mechanics
The lens cannot mechanically exceed its 1:1 internal reproduction design. However, because flat port refraction compresses the diagonal field of view by $25\%$ to $33\%$ (narrowing from $20^\circ$ in air down to $15^\circ$ in water), a smaller spatial area of the subject fills the sensor. This results in a frame-filling, practical magnification of **$1.33\times$** underwater ($2.66\times$ full-frame equivalence), allowing a tiny $9.8 \text{ mm} \times 12.8 \text{ mm}$ subject area to fill the entire frame.

---

## 4. Wet Close-Up Optics & Focus Optimizers

For subjects smaller than 10 mm, or to expand performance across wider working distances, external wet diopters can be mounted via the M67 front port threads:

* **Nauticam CMC-2:** Delivers moderate magnification ($\sim1.7\times$) with an accessible working distance range of $3.3 \text{ cm}$ to $12.2 \text{ cm}$. Ideal for general macro field handling.
* **Nauticam CMC-1:** Tailored for ultra-high magnification details ($\sim2.3\times$) with a highly compressed practical working distance of $2.0 \text{ cm}$ to $5.0 \text{ cm}$.
* **Nauticam SMC-3:** Features ultra-low dispersion glass optimized for super-macro imaging, delivering a $2.3\times$ magnification factor across a stabilized $5.0 \text{ cm}$ to $10.0 \text{ cm}$ working range.
* **Nauticam MFO-1 (Mid-Range Focus Optimizer):** Corrects flat-port optical aberrations (pincushion distortion, chromatic fringing, and edge blur) by restructuring the light path. It eliminates autofocus hunting, improves corner sharpness, and scales maximum usable working distances out to $1.14 \text{ meters}$ for skittish marine subjects.

---

## 5. Technical Field Practices & Settings

1. **Focus Limiter Constraints:** Pre-set the lens's physical focus limit switch to the **$0.19\text{ m–}0.4\text{ m}$** boundary zone prior to sealing the housing. Submerged refraction shifts this range into a practical subject-to-sensor distance of **$22 \text{ cm}$ to $53 \text{ cm}$** in water, accelerating autofocus acquisition by blocking the lens from hunting into open water.
2. **Back-Button Autofocus Alignment:** Map the camera's AF-ON function to an ergonomic thumb lever on the housing. This separates focus from the shutter release, enabling the "lock and rock" technique—locking focus mechanically and making microscopic physical adjustments by moving slightly forward or backward to pinpoint critical depth-of-field placement on the subject's eye.
3. **Aperture & Diffraction Management:** Maintain working apertures between **$f/5.6$ and $f/11$** to maximize depth of field while avoiding image degradation from optical diffraction. For deep macro focus fields, deploy the OM-1 Mark II’s automated in-camera focus stacking engine.
