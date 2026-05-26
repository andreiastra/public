# Test Shot Diagnostic: Fisheye Hyperfocal Physics (P5268721.jpg)

This document analyzes the EXIF metadata and optical physics of the indoor test [shot](./P5268721.jpg), demonstrating why a wide-open aperture of f/1.8 on an 8mm fisheye lens does not inherently produce a shallow depth of field.

---

## 1. EXIF Metadata Breakdown

The test shot captured on May 26, 2026, utilizes the baseline exposure parameters established for the upcoming wide-angle Custom Mode (C2):

* **Camera Body:** OM SYSTEM OM-1 Mark II (Serial: BJRA41690)
* **Lens:** M.ZUIKO DIGITAL ED 8mm f/1.8 Fisheye PRO (Serial: 347001996)
* **Focal Length:** 8mm (16mm full-frame equivalent)
* **Aperture:** f/1.8
* **Shutter Speed:** 1/100s
* **ISO:** 200
* **Exposure Mode:** Manual
* **Metering Mode:** Spot

---

## 2. The Optical Paradox: Why f/1.8 is Not Shallow

In portrait or macro photography, an aperture of f/1.8 creates a razor-thin depth of field with heavy background isolation. However, in **P5268721.jpg**, the entire room—from your feet in the immediate foreground, to the camera rig on the chair, to the text on the monitor and the curtains in the background—is completely sharp. 

This occurs due to two compounding optical principles:

### Extreme Short Focal Length (8mm)
Depth of field is exponentially dictated by focal length. An 8mm lens has massive inherent depth of field compared to a standard 60mm macro lens, even when the physical aperture iris is wide open.

### Hyperfocal Distance Dynamics
The hyperfocal distance is the closest distance at which a lens can be focused while keeping objects at infinity acceptably sharp.
* At **8mm** and **f/1.8** on a Micro Four Thirds sensor, the hyperfocal distance is incredibly short: **approximately 2.4 meters (under 8 feet)**.
* Because the lens was focused on the middle of the room (the chair/desk area roughly 1.5 to 2 meters away), the depth of field expanded to wrap around almost the entire environment. Mathematically, everything from roughly 1.1 meters out to infinity falls into acceptable focus.

---

## 3. Underwater Tactical Application: Forcing Bokeh

This test confirms that **f/1.8 will not provide background separation underwater if your subject is a few feet away.** To successfully break the hyperfocal wrap and isolate a subject (such as an environmental marine life portrait) against a blurred water column, you must dramatically manipulate the subject-to-lens distance:

* **The Centimeter Rule:** You must physically position the dome port glass **within 10 to 20 centimeters** of your primary subject. 
* **The Collapse of DoF:** Bringing the focus plane this close to the front lens element forces the depth of field to collapse down to a matter of centimeters. 
* **The Result:** The immediate foreground subject remains tack-sharp in the center of the frame, while the entire background reef structure or water column completely melts away into smooth, ambient green or blue bokeh.
