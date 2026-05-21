# Custom Mode C1: Underwater Macro Settings & Spatial Profile
**System:** OM SYSTEM OM-1 Mark II | M.Zuiko 60mm F2.8 Macro | Nauticam Housing
**Strobe Rig:** Backscatter Mini Flash 2 (MF-2) & Backscatter OM Smart Trigger

---

## 📌 Critical Pre-Dive Lens Configuration
The M.Zuiko 60mm Macro lens features an internal focusing mechanism, meaning its physical barrel does not extend during use. However, its mechanical focus limiter switch is completely inaccessible once sealed inside the housing.

* **Land-Locked Setting:** **`0.19m - 0.4m` (Macro Range)**
* **Operational Intent:** This hard physical constraint must be set on land. It restricts the autofocus elements from sweeping all the way out to infinity, dramatically speeding up autofocus acquisition in low-light, low-visibility, or high-surge environments.

---

## 🌊 In-Water Spatial Boundaries (Working Distance)
Due to refraction, water alters visual perception by making subjects appear $33\%$ closer and larger than they actually are. However, the physical mechanics of the lens remain constant. 

Measuring the clear water gap **from the front surface of the flat port glass to the subject**, your exact operating envelope is:

* ### 🛑 MINIMUM DISTANCE: `5.0 cm – 6.0 cm`
    * **Magnification:** Peak $1:1$ Life-Size Macro ($2:1$ Full Frame equivalent).
    * **Tactical Consideration:** At this close proximity, the housing port will cast a shadow over the subject. Strobes must be pulled tight to the housing grips and aggressively angled inward. The high-intensity LED focus light on the MF-2 is mandatory to provide the contrast needed for `S-AF` at small apertures.
* ### 🗺️ MAXIMUM DISTANCE: `29.0 cm`
    * **Focus Limitation:** The absolute cutoff point dictated by your dry-land $0.4\text{m}$ limiter switch.
    * **Tactical Consideration:** If a subject is further than a standard ruler's length ($29\text{ cm}$) from your port glass, the autofocus system will instantly reject it and refuse to hunt into open blue water. You must physically move closer to engage focus.

---

## ⚙️ Complete Profile Architecture

### Camera & Optics
* **Camera Body:** OM SYSTEM OM-1 Mark II
* **Lens:** M.Zuiko 60mm F2.8 Macro
* **Housing Port:** Standard Nauticam Flat Macro Port

### Exposure Settings
* **Mode:** Manual (M)
* **Aperture:** `f/11` – `f/14` (**The "Secret Handshake" Strategy**)
    * *f/11:* Maximizes peak optical sharpness for stationary subjects.
    * *f/14:* Optimal diffraction compromise for Micro Four Thirds; yields $50\%$ more depth of field (DOF) than $f/9$ while avoiding the image softness ("mush") that sets in past $f/16$.
* **Shutter Speed:** `1/250s` (Maximum strobe synchronization limit)
* **ISO:** `200` (Base crispness, lowest noise floor)

### Focus & Drive
* **AF Mode:** Single AF (S-AF)
* **AF Illuminator:** OFF (Relies entirely on strobe-mounted focus lights)
* **AF Target:** Small Single Point (For precise positioning on a nudibranch's rhinophore or a shrimp's eye)
* **AF+MF:** OFF *(Nauticam O60-F Focus Gear omitted for this configuration)*
* **Back Button Focus:** ON (Assigned to `AF-ON`)
* **Shutter Half-press:** AF On *(Kept active for now as a hybrid safety layer)*
* **Release Priority S-AF:** OFF (Ensures the camera never fires unless true focus lock is achieved)
* **Drive Mode:** Single Shot
* **Image Stabilization:** S-IS1 (Body-only stabilization optimized for macro movement)

### Flash & Lighting Control
* **Strobe:** Backscatter Mini Flash 2 (MF-2)
* **Trigger:** Backscatter OM Smart Trigger
* **Camera Menu:** Flash Fill-In (`RC Mode ON` for advanced optical communication)
* **Strobe Dial:** **SC Macro** (Smart Control Macro)
* **Flash Mode:** TTL / SC Macro
* **Diffuser:** Flat White Diffuser
* **LED Intensity:** High (Critical for providing target contrast at micro working distances)

### Ergonomics & Focus Aids
* **Fn Lever Customization:** 1.  *Position 1:* Aperture (`FNo`) & Shutter Speed
    2.  *Position 2:* Flash Exposure Compensation & ISO
* **Metering Mode:** Spot (Exposes purely for the macro subject, ignoring dark ambient backgrounds)
* **Picture Mode:** Natural
* **Focus Peaking:** OFF (Can be toggled ON via a mapped housing button for high-contrast night scenarios)
* **MF Assist / Magnify:** OFF (Explicitly mapped to a housing button for manual verification to prevent automated, disorienting magnification shifts during ocean surge)
