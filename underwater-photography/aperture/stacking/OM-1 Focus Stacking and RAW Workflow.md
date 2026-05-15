# **Technical Integration and Workflow Analysis of the OM-1 Mark II Underwater System for Advanced Macro Photography**

The arrival of the OM System OM-1 Mark II has precipitated a profound transformation in the technical landscape of underwater macro photography. By synthesizing high-speed stacked sensor architecture with advanced computational algorithms, the platform addresses the most persistent challenge in the marine environment: the physical limitation of depth of field at high magnifications. This report provides an exhaustive analysis of the OM-1 Mark II system, specifically configured within a Nauticam NA-OM1 II housing and supported by Backscatter Hybrid Flash lighting. The investigation focuses on the synergy between optical hardware, computational focusing mechanics, and a rigorous RAW-centric post-processing workflow.

## **Hardware Foundations and Computational Potential**

The transition from the original OM-1 to the Mark II iteration was characterized by a significant expansion of internal memory resources, which functions as the primary catalyst for enhanced computational performance.1 At the heart of this system is the 20.4-megapixel Stacked BSI Live MOS sensor, a component that enables a data readout speed previously unattainable in the Micro Four Thirds format.2 For the underwater professional, this speed is not merely a theoretical metric; it is the prerequisite for focus stacking at burst rates that can freeze the micro-movements of both the photographer and the subject in a dynamic liquid medium.4 The TruePic X processor acts as the engine for this data, managing the complex phase-detection AF calculations across 1,053 cross-type points.2 In the context of macro photography, where focus must often be achieved on a subject's eye that is only a few millimeters in diameter, the Cross Quad Pixel AF system provides a level of reliability that minimizes "focus hunting" in the low-contrast, low-light conditions common beneath the thermocline.2

The physical construction of the OM-1 Mark II also contributes to its underwater viability. The body carries an IP53 weather-sealing rating, which, while often viewed as a "topside" feature, is a critical second line of defense within a Nauticam housing.2 Underwater housings are subject to internal humidity and potential minor leaks; the environmental sealing of the camera body ensures that the internal electronics remain protected from salt-air corrosion and condensation.7 Furthermore, the introduction of a rubberized mode dial on the Mark II body suggests an awareness of the tactile requirements of photography, ensuring that the dial interfaces securely with the mechanical gears of the Nauticam housing.1

| Feature | Specification | Underwater Significance |
| :---- | :---- | :---- |
| Sensor Type | 20.4MP Stacked BSI Live MOS | High-speed readout for focus stacking and blackout-free viewing. |
| AF Points | 1,053 Cross-type Phase Detection | Essential for tracking skittish macro subjects in low light. |
| In-Body Image Stabilization | 8.5 EV Stops | Facilitates handheld focus stacking in surge and current. |
| Processor | TruePic X Dual Quad-Core | Drives AI Subject Detection and rapid computational rendering. |
| Weather Sealing | IP53 Rated | Protects against housing humidity and environmental stressors. |

2

## **Optical Engineering and the Macro Paradigm**

The effectiveness of any focus stacking system is inextricably linked to the optical performance and motor speed of the lens in use. The M.Zuiko macro lineup, particularly the 60mm f/2.8 and the 90mm f/3.5 IS PRO, provides the necessary focal lengths to address a variety of underwater subject scales.

### **The M.Zuiko Digital ED 60mm f/2.8 Macro**

The 60mm macro lens remains a staple of the underwater professional due to its compact size and 1:1 magnification ratio.8 One of its most significant features is the focus limiter switch, which includes a spring-loaded 1:1 shortcut.8 In an underwater setting, where manual manipulation of the lens barrel is restricted by the housing, the ability to utilize the Nauticam’s control levers to snap the lens to its minimum focus distance is a significant ergonomic advantage.8 This allows the photographer to establish a consistent starting point for focus stacks, ensuring that the nearest point of the subject is always within the initial depth-of-field slice.9

### **The M.Zuiko Digital ED 90mm f/3.5 Macro IS PRO**

The 90mm f/3.5 IS PRO represents the zenith of Micro Four Thirds macro optics, offering up to 2x magnification, which translates to a 4x full-frame equivalent.6 This extreme magnification introduces complex optical behaviors that must be understood to optimize focus stacking. Technical analysis reveals that as magnification increases, the effective aperture of the lens changes significantly.11

| Magnification | Nominal Aperture | Effective Aperture | DOF (mm) at Differential \= 1 |
| :---- | :---- | :---- | :---- |
| 2.0x (S-Macro) | f/5.0 | f/8.0 | 0.126 mm |
| 1.0x | f/3.5 | f/4.5 | 0.19 mm |
| 0.5x | f/3.5 | f/4.0 | 0.5 mm |

11

The phenomenon of effective aperture is critical for the underwater photographer because it influences the amount of strobe light required for a proper exposure. At 2x magnification, a nominal aperture of f/5.0 behaves like f/8.0 in terms of light gathering and diffraction.11 This necessitates a strategy where strobe power is increased or ISO is raised to maintain the 1/100s sync speed required for the OM-1 Mark II’s electronic shutter during focus stacking.12 Furthermore, the thinness of the depth of field at 2x magnification (0.126mm per slice) explains why a narrow focus differential is mandatory for high-magnification subjects.11

## **Mechanics of Computational Focusing: Stacking vs. Bracketing**

The OM-1 Mark II offers two distinct methods for expanding depth of field: in-camera Focus Stacking and Focus Bracketing for external processing. The choice between these modes depends on the depth of the subject and the desired final output quality.

### **In-Camera Focus Stacking**

Focus Stacking is a computational mode where the camera captures a sequence of 3 to 15 images and merges them internally into a single JPEG.5 The system automatically shifts the focus point forwards and backwards from the initial focus position to cover the subject.14 A critical limitation of this mode is the 7% crop factor; the camera requires this buffer to align the images if there has been slight movement between frames.10

Underwater, the 15-shot limit of the Mark II is a significant improvement over the 8-shot limit of earlier models like the E-M1 Mark II, yet it may still be insufficient for deep subjects at high magnification.15 If a subject like a Longnose Hawkfish is positioned at an angle, 15 shots at a narrow differential may only cover the head and mid-body, leaving the tail blurred.16 However, the advantage of this mode is immediate verification; the photographer can review the rendered composite on the monitor to ensure that the critical areas are in focus before the subject departs.13

### **Focus Bracketing and RAW Flexibility**

For subjects requiring more than 15 slices of focus, the Focus Bracketing mode allows for up to 999 frames to be captured in a single burst.4 This mode does not attempt an internal merge, meaning there is no 7% crop and no JPEG-only restriction.16 The camera saves every individual frame as a RAW (.ORF) file, providing maximum latitude for post-processing.17

The primary challenge of Focus Bracketing underwater is the massive amount of data generated. A 50-shot bracket for a single nudibranch can result in over 1GB of RAW data.4 Managing this workflow requires a high-speed UHS-II SD card to prevent the camera's buffer from clogging, especially when using the "SH2" burst mode which can reach 50 fps with compatible lenses.5

## **Optimization of the Focus Differential Setting**

The "Focus Differential" setting, adjustable from 1 to 10, is the most misunderstood variable in the OM System.17 It does not represent a fixed distance but rather a step size relative to the lens’s current focal length, aperture, and focus distance.11

### **The Interplay of Aperture and Differential**

In focus stacking, a small differential (1-3) results in significant overlap between the slices of focus.12 This overlap is essential for a clean merge, as it provides the algorithm with enough data to transition between sharp and blurred regions without creating "focus bands" or "ghosting" artifacts.12 Conversely, a wide differential (8-10) is typically used for landscape-style macro or when the subject is far from the lens.12

For underwater macro, the consensus among experts is to use an aperture between f/5.6 and f/8.0 in combination with a narrow differential.12 While a single shot at f/22 would provide more depth of field, it would be severely degraded by diffraction.18 By stacking 10 shots at f/5.6, the photographer achieves the depth of field of f/32 but maintains the optical resolution and "pop" of f/5.6.18

| Subject Complexity | Recommended Differential | Rationale |
| :---- | :---- | :---- |
| Super Macro (2x) | 1 | Depth of field is sub-millimeter; any gap will ruin the stack. |
| Textural Macro (1x) | 2-3 | Balances frame count with smooth transitions. |
| Fish Portraits | 4-5 | Allows for fewer shots, reducing the risk of subject movement. |
| Environmental Macro | 7-9 | Useful when the subject is small in the frame and background detail is needed. |

11

## **Lighting Integration with Backscatter Hybrid Flash**

Lighting is the most significant constraint in underwater focus stacking. Because the OM-1 Mark II uses an electronic shutter for these modes, the flash sync speed is limited to 1/100s.12 This limitation requires a strobe that can fire rapidly, consistently, and accurately over a burst of 10 to 15 shots.

### **The Backscatter Smart Control (SC) System**

The Backscatter Hybrid Flash utilizes a proprietary "Smart Control" (SC) protocol designed specifically for the OM/Olympus RC system.7 Unlike traditional "mimic" TTL, which simply copies the duration of the camera's trigger, the SC system uses a digital code sent via fiber optic cable to command the strobe to a precise power level.22 This ensures that every frame in a focus stack has an identical exposure, preventing the "flicker" effect that occurs if a strobe’s output varies during a burst.7

The Hybrid Flash features two SC modes:

* **Standard SC:** Optimized for larger subjects and fish portraits.7  
* **SC Macro:** Calibrated for subjects within 18 inches of the port, preventing the overexposure common in macro TTL systems.7

### **Recycle Kinetics and Thermal Management**

The ability of the Hybrid Flash to keep up with the OM-1 Mark II’s 10-50 fps burst rates is a function of its capacitor design and 21700 battery power source.7 At Power Level F (GN 29), the strobe recycles in approximately 0.67 seconds.24 However, for a 15-shot stack at 10 fps, the strobe must fire much faster. This is achieved by using a lower power setting (e.g., 1/8th or 1/16th power), where the strobe does not fully deplete its capacitor for each shot.23

| Power Level | Guide Number | Recycle Time (Full Discharge) | Burst Capability |
| :---- | :---- | :---- | :---- |
| \+2 | 40 | 1.67 s | Single shot or slow burst. |
| \+1 | 34 | 0.87 s | Medium sequential. |
| F | 29 | 0.67 s | High-speed stacking (10 fps). |
| 1/8 | \~10 | \< 0.1 s | Ultra-high-speed (30 fps). |

23

A critical consideration for the equipment manager is the thermal protection circuit of the Hybrid Flash. Rapid firing at high power levels generates significant heat. If the strobe reaches its threshold, it will emit a long beep and flash a purple indicator, automatically reducing power by 0.5 stops to prevent damage.7 For focus stacking, it is always recommended to use the lowest power level possible and compensate with ISO 200 or 400 to keep the strobe cool and the recycles instantaneous.12

## **Ergonomics and Housing Configuration: The Nauticam NA-OM1 II**

The transition from camera to underwater housing requires a strategic reassignment of button roles to ensure that computational modes can be activated without removing the hands from the housing grips. Nauticam’s engineering provides direct mechanical access to the most vital OM-1 Mark II controls.2

### **The Back-Button Focus Strategy**

In underwater macro, the "Lock it and Rock it" technique is the standard for success.28 This involves separating the focusing function from the shutter button—a technique known as Back-Button Focus.28 By assigning the focus function to the AF-ON button (accessible via a dedicated thumb lever on the Nauticam housing) and disabling focus on the shutter button, the photographer gains absolute control over the stack's starting point.28

1. **Selection:** Set the camera to S-AF or S-AF+MF.7  
2. **Acquisition:** Use the AF-ON lever to lock focus on the nearest point of the subject (e.g., the rhinoceros shrimp’s rostrum).9  
3. **Refinement:** If using S-AF+MF, the photographer can fine-tune the focus by rotating the lens gear on the Nauticam housing while watching the Focus Peaking or Magnify assist.7  
4. **Execution:** Once focus is locked, the photographer gently rocks forward or waits for the subject to enter the critical plane, then fully depresses the shutter to initiate the automated stack.28

### **Custom Mode Dial Assignments**

Navigating the OM-1 Mark II’s deep menu system while underwater is impractical. The use of the C1 through C4 custom modes on the mode dial is the only efficient way to manage a high-end setup.7

| Custom Mode | Primary Use Case | Key Settings |
| :---- | :---- | :---- |
| **C1** | Standard Macro | M Mode, f/11, 1/250s, ISO 200, S-AF, Single Shot. |
| **C2** | In-Camera Stack | M Mode, f/8, 1/100s, ISO 200, Focus Stacking On (15 shots, FD 3). |
| **C3** | Super Macro Bracket | M Mode, f/5.6, 1/100s, ISO 400, Focus BKT On (30 shots, FD 2). |
| **C4** | Blackwater / Action | M Mode, f/8, 1/250s, ISO 200, C-AF+TR, Pro Capture. |

7

By saving these configurations, the equipment manager ensures that the photographer can pivot from a single-shot portrait to a 15-frame stack with a single click of the mode dial.7

## **Professional RAW Workflow and Asset Management**

A high-end macro setup generates a volume of data that can overwhelm traditional photography workflows. A single day of diving with focus bracketing can produce over 2,000 RAW files. Efficient management of this data is essential to maintain image quality and prevent "workflow fatigue."

### **OM Workspace and USB RAW Processing**

OM Workspace is the foundational software for this system, offering a unique "USB RAW Processing" feature.7 By connecting the OM-1 Mark II to a computer via a USB-C cable, the software offloads the heavy mathematical processing of RAW development to the camera’s TruePic X chip. This is significantly faster than using a computer’s CPU and ensures that the camera's proprietary color science and noise reduction algorithms are applied exactly as they would be in-camera.

For focus stacking, OM Workspace provides a dedicated "Focus Stacking" tool in the "Tools" menu.30 The workflow involves:

1. **Importing:** Bringing in the.ORF files using the "Import from Camera" function.30  
2. **Selection:** Using the "Focus Analyzer" to automatically sort the frames by sharpness, allowing the photographer to quickly identify the keepers from a long bracket.29  
3. **Compositing:** Selecting the range of sharp frames and clicking "Composite".30  
4. **Alignment:** Selecting "Adjust Image Position" to compensate for the micro-movements of the photographer during the underwater burst.30

### **Advanced Stacking: Helicon Focus and Zerene Stacker**

While OM Workspace is excellent for simple stacks, it lacks the advanced masking and retouching tools required for complex underwater scenes (e.g., a shrimp hidden behind coral branches).4 Professional macro photographers often transition to Helicon Focus or Zerene Stacker.4

Helicon Focus has been updated to support the OM-1 Mark II's.ORF files directly, eliminating the need for a DNG conversion step.32 The advantage of these third-party tools is the "Method B" (Depth Map) or "Method C" (Pyramid) algorithms, which are often better at handling the "bokeh artifacts" that occur when a foreground object moves slightly during the stack.4

### **The Role of the ORI File**

When shooting in RAW+JPEG during Focus Stacking, the camera may generate a file with the.ORI extension.19 This is a standard RAW file containing the data from the first image in the sequence.19 If the in-camera merge fails or produces a "Focus Stacking Error" due to excessive movement, the photographer can simply rename the.ORI file to.ORF.19 This acts as a safety net, ensuring that even if the computational process fails, the photographer still has a high-quality single-shot RAW of the subject.19

## **Advanced Field Techniques: Overcoming Environmental Obstacles**

The marine environment introduces variables—surge, current, and low visibility— that are not present in terrestrial macro photography. Mastering the OM-1 Mark II requires techniques tailored to these physics.

### **Blackwater and Night Macro Tactics**

In the mid-water environment of a blackwater dive, subjects are often translucent and in constant motion.1 The OM-1 Mark II’s "S-OVF" (Simulated Optical Viewfinder) is a critical setting here.5 Unlike a standard EVF, which reflects the camera’s exposure settings, S-OVF provides a view similar to an optical SLR, showing a bright, clear subject regardless of the aperture or shutter speed.5 This allows the photographer to track fast-moving planktonic subjects without the "darkening" effect of f/11 or the lag of low-light electronic gain.12

Additionally, the AI Subject Detection for "Birds" or "Dogs & Cats" can sometimes be adapted for marine life.2 While not specifically calibrated for nudibranchs, the "Human" eye detection mode is often effective at locking onto the eyes of fish or cephalopods, providing a starting point for a focus stack that ensures the most critical part of the subject is sharp.6

### **Diffraction Limits and Optical Reality**

A common error in underwater macro is the use of extremely small apertures (f/22 or smaller) to gain depth of field.20 On a Micro Four Thirds sensor, diffraction begins to soften the image at apertures smaller than f/8.0.11 The primary "third-order insight" of this report is that Focus Stacking is not just a tool for more depth; it is a tool for *better* depth. By using a stack of 15 images at f/5.6, the photographer achieves the depth of field of f/32 without ever crossing the diffraction threshold, resulting in an image that is both deeply sharp and optically crisp.18

### **Remote Lighting and the Light Pipe**

For creative macro, moving the Hybrid Flash off the camera is essential.7 The Backscatter Remote Lighting System uses a "Light Pipe" attached to the remote strobe to catch the optical signal from the on-camera flash.7

* **The Workflow:** The on-camera strobe is set to Manual (M), while the remote strobe is set to REM (Remote).7  
* **The Control:** The photographer can change the power of the remote strobe wirelessly by holding the "Test" button on the main strobe, which sends a digital pulse to the remote unit.7  
* **The Stacking Benefit:** Because this system is optical and instantaneous, it allows for off-camera side-lighting or back-lighting during a 50 fps focus bracket, ensuring that every frame is lit from the desired angle.7

## **System Maintenance and Reliability Protocols**

A high-end system representing a significant investment must be maintained with precision to prevent catastrophic failure in the field.

### **O-Ring Science and Battery Safety**

The Backscatter Hybrid Flash utilizes a three-layer sealing system: two main O-rings and a sand seal gasket.7

* **The Sand Seal:** This is not a watertight seal but a debris barrier. It must never be greased, as grease attracts the very sand it is designed to exclude.7  
* **Lubrication:** Only the provided silicone grease should be used on the two main O-rings. Petroleum-based lubricants like WD-40 will cause the O-rings to swell and fail.7  
* **Battery Management:** The 21700 batteries (e.g., Nitecore NL2153HP) are high-discharge cells. They should never be transported inside the strobe during travel.7 If the battery compartment shows any signs of water intrusion or corrosion, the unit must be immediately dried and serviced by an authorized dealer.7

### **Housing Humidity and Pressure Testing**

The Nauticam NA-OM1 II is equipped with a vacuum check and leak detection system. This is a non-negotiable requirement for the equipment manager. Before every dive, a vacuum should be drawn on the housing and monitored for at least 20 minutes.7 This ensures that the integrity of every O-ring—including the complex sync cord bulkheads and port seals—is confirmed before the system is exposed to depth.7

## **Conclusions and Technical Recommendations**

The integration of the OM System OM-1 Mark II, Nauticam housing, and Backscatter lighting represents a comprehensive solution for the most demanding underwater macro scenarios. To maximize the performance of this setup, the following technical protocols are recommended:

1. **Prioritize RAW Focus Bracketing** for any subject requiring maximum magnification (1:1 or 2:1) or significant depth, as the 15-frame in-camera limit is often insufficient for professional-grade rendering at these scales.  
2. **Standardize on Focus Differential 2 or 3** for general macro, only moving to 1 for ultra-magnification subjects. This ensures a reliable merge while minimizing frame counts.  
3. **Utilize the 1/100s Sync Speed Constraint** as a creative prompt. In high-ambient-light scenarios, use smaller apertures (f/11) to manage the background, but rely on the stack to maintain foreground sharpness.  
4. **Adopt a "One-Touch" Workflow** by assigning Focus Stacking and Focus Bracketing to the Custom Mode dial. This eliminates menu-diving and allows the photographer to focus entirely on buoyancy and composition.  
5. **Leverage USB RAW Processing** in OM Workspace to handle the high volume of bracketed frames, ensuring that the camera's hardware-accelerated processing is used for development.  
6. **Implement the Smart Control (SC) System** for all macro lighting. The accuracy of the SC Macro mode is the only reliable way to achieve consistent exposures during the high-speed bursts required for computational focusing.

Through the mastery of these second-order relationships—between strobe recycle times and shutter sync, between magnification and effective aperture, and between computational algorithms and RAW flexibility—the underwater photographer can transcend the traditional physical limits of the medium. The OM-1 Mark II system, when properly managed, provides a level of detail and clarity that was previously the sole domain of the most sophisticated land-based macro studios.

#### **Works cited**

1. OM-1 MkII announced \- Photography Gear and Technique \- WaterPixels, accessed May 5, 2026, [https://waterpixels.net/forums/topic/813-om-1-mkii-announced/](https://waterpixels.net/forums/topic/813-om-1-mkii-announced/)  
2. OM Systems OM-1 Mirrorless Camera with 12-40mm Pro II Lens \- Backscatter.com, accessed May 5, 2026, [https://www.backscatter.com/Olympus-OM-1-Mirrorless-Camera-with-12-40mm-Pro-II-Lens](https://www.backscatter.com/Olympus-OM-1-Mirrorless-Camera-with-12-40mm-Pro-II-Lens)  
3. OM Systems OM-1 Mirrorless Camera Body \- Backscatter Underwater Video & Photo, accessed May 5, 2026, [https://www.backscatter.com/Olympus-OM-1-Mirrorless-Camera-Body](https://www.backscatter.com/Olympus-OM-1-Mirrorless-Camera-Body)  
4. Embarking on a Macro Photography Journey with the OM-1 Mark II, accessed May 5, 2026, [https://learnandsupport.getolympus.com/learn-center/photography-tips/macro/embarking-on-a-macro-photography-journey-with-the-om-1-mark-ii](https://learnandsupport.getolympus.com/learn-center/photography-tips/macro/embarking-on-a-macro-photography-journey-with-the-om-1-mark-ii)  
5. OM System OM-1 II Mirrorless Camera Body \- Backscatter.com, accessed May 5, 2026, [https://www.backscatter.com/OM-System-OM-1-II-Mirrorless-Camera-Body](https://www.backscatter.com/OM-System-OM-1-II-Mirrorless-Camera-Body)  
6. Dive Into Underwater Photography \- OM SYSTEM LEARN CENTER, accessed May 5, 2026, [https://learnandsupport.getolympus.com/learn-center/photography-tips/underwater/dive-into-underwater-photography](https://learnandsupport.getolympus.com/learn-center/photography-tips/underwater/dive-into-underwater-photography)  
7. OM-1\_Mark\_II\_MANUAL\_EN.pdf  
8. Mastering the 60mm Macro \- OM SYSTEM LEARN CENTER, accessed May 5, 2026, [https://learnandsupport.getolympus.com/learn-center/photography-tips/macro/mastering-the-60mm-macro](https://learnandsupport.getolympus.com/learn-center/photography-tips/macro/mastering-the-60mm-macro)  
9. OM-1 & OM-1 Mark II: Focus Stacking Explained with Chris McGinnis \- YouTube, accessed May 5, 2026, [https://www.youtube.com/watch?v=7li\_p6zXqhQ](https://www.youtube.com/watch?v=7li_p6zXqhQ)  
10. Which lenses are compatible with the Focus Stacking mode? | OM SYSTEM, accessed May 5, 2026, [https://learnandsupport.getolympus.com/support/e-m1-mark-ii/which-lenses-are-compatible-with-the-focus-stacking-mode](https://learnandsupport.getolympus.com/support/e-m1-mark-ii/which-lenses-are-compatible-with-the-focus-stacking-mode)  
11. The nitty-gritty details of macrophotography \- Photo Rumblings and Whispers, accessed May 5, 2026, [https://www.photo-spectrum.info/pages/cameras/OM1-focus-bracketing.html](https://www.photo-spectrum.info/pages/cameras/OM1-focus-bracketing.html)  
12. How to setup your OM SYSTEM camera for focus bracketing and focus stacking \- wildmacro, accessed May 5, 2026, [https://wildmacro.de/how-to-setup-your-om-system-camera-for-focus-bracketing-and-focus-stacking/](https://wildmacro.de/how-to-setup-your-om-system-camera-for-focus-bracketing-and-focus-stacking/)  
13. Increasing Depth of Field (Focus Stacking) \- Camera How To, accessed May 5, 2026, [https://learning.omsystem.com/OM-1MarkII/zz\_html\_manual/en/focus\_stacking\_144.html](https://learning.omsystem.com/OM-1MarkII/zz_html_manual/en/focus_stacking_144.html)  
14. OM-1 & OM-1 Mark II Settings: Focus stacking \- YouTube, accessed May 5, 2026, [https://www.youtube.com/watch?v=c5qxPdUTVjQ](https://www.youtube.com/watch?v=c5qxPdUTVjQ)  
15. Focus Stacking and Bracketing \- Creative Island Photography, accessed May 5, 2026, [https://www.creativeislandphoto.com/blog/focus-stacking-and-bracketing](https://www.creativeislandphoto.com/blog/focus-stacking-and-bracketing)  
16. FOCUS STACKING & BRACKETING WITH OM-D \- Photography Journal\_en \- Blog, accessed May 5, 2026, [https://my.omsystem.com/blog/b/photography-journal\_en/posts/focus-stacking-bracketing-with-om](https://my.omsystem.com/blog/b/photography-journal_en/posts/focus-stacking-bracketing-with-om)  
17. OM-1 & OM-1 Mark II Settings: Focus bracketing \- YouTube, accessed May 5, 2026, [https://www.youtube.com/watch?v=A1Rj1zWIues](https://www.youtube.com/watch?v=A1Rj1zWIues)  
18. Some thoughts on Focus Stacking using the OM-1 | luxBorealis Blog, accessed May 5, 2026, [https://blog.luxborealis.com/2023/08/04/some-thoughts-on-focus-stacking-using-the-om-1/](https://blog.luxborealis.com/2023/08/04/some-thoughts-on-focus-stacking-using-the-om-1/)  
19. Q\&A for OM-1 Mark II, accessed May 5, 2026, [https://support.jp.omsystem.com/en/support/imsg/digicamera/qa/products/om1m2/](https://support.jp.omsystem.com/en/support/imsg/digicamera/qa/products/om1m2/)  
20. Best Underwater Settings for the Olympus OM-D E-M1 Mark II Camera, accessed May 5, 2026, [https://www.uwphotographyguide.com/olympus-omd-em1-markii-best-underwater-settings/](https://www.uwphotographyguide.com/olympus-omd-em1-markii-best-underwater-settings/)  
21. Macro Photography | OM-1 Mark II & M.Zuiko 60mm f/2.8 \- espenhelland.com, accessed May 5, 2026, [https://espenhelland.com/macro-photography-om-1-mark-ii-m-zuiko-60mm-f-2-8/](https://espenhelland.com/macro-photography-om-1-mark-ii-m-zuiko-60mm-f-2-8/)  
22. Backscatter Smart Control TTL LED Universal Flash Trigger for OM System & Olympus, accessed May 5, 2026, [https://www.backscatter.com/Backscatter-Smart-Control-TTL-LED-Universal-Flash-Trigger-for-OM-System-Olympus](https://www.backscatter.com/Backscatter-Smart-Control-TTL-LED-Universal-Flash-Trigger-for-OM-System-Olympus)  
23. Backscatter Hybrid Flash Underwater Strobe & Video Light Review, accessed May 5, 2026, [https://www.backscatter.com/reviews/post/Backscatter-Hybrid-Flash-Underwater-Strobe-Video-Light-Review](https://www.backscatter.com/reviews/post/Backscatter-Hybrid-Flash-Underwater-Strobe-Video-Light-Review)  
24. Backscatter Hybrid Flash Final Review \- The Underwater Club, accessed May 5, 2026, [https://theunderwaterclub.com/blog/backscatter-hybrid-flash-final-review/](https://theunderwaterclub.com/blog/backscatter-hybrid-flash-final-review/)  
25. Backscatter Hybrid Flash Single Underwater Strobe & Ultralight Arm Package, accessed May 5, 2026, [https://www.backscatter.com/Backscatter-Hybrid-Flash-Single-Underwater-Strobe-Ultralight-Arm-Package](https://www.backscatter.com/Backscatter-Hybrid-Flash-Single-Underwater-Strobe-Ultralight-Arm-Package)  
26. Backscatter-Hybrid-Flash-Instruction-Manual.pdf, accessed May 5, 2026, [https://www.backscatter.com/images/article/content/Hybrid-Flash/Backscatter-Hybrid-Flash-Instruction-Manual.pdf](https://www.backscatter.com/images/article/content/Hybrid-Flash/Backscatter-Hybrid-Flash-Instruction-Manual.pdf)  
27. NA-RX100VI: Komodo and Whalesharks \- Nauticam, accessed May 5, 2026, [https://www.nauticam.com/blogs/news/na-rx100vi-komodo-and-whalesharks](https://www.nauticam.com/blogs/news/na-rx100vi-komodo-and-whalesharks)  
28. Back Button Focus \- Nauticam, accessed May 5, 2026, [https://www.nauticam.com/blogs/news/back-button-focus](https://www.nauticam.com/blogs/news/back-button-focus)  
29. OM Workspace image editing software | OM Digital Solutions Corporation, accessed May 5, 2026, [https://software.omsystem.com/omworkspace/](https://software.omsystem.com/omworkspace/)  
30. OM Workspace: A Beginner's Guide, accessed May 5, 2026, [https://learnandsupport.getolympus.com/learn-center/photography-tips/technique/om-workspace-a-beginners-guide](https://learnandsupport.getolympus.com/learn-center/photography-tips/technique/om-workspace-a-beginners-guide)  
31. OM System Focus Bracketing Tutorial \- YouTube, accessed May 5, 2026, [https://www.youtube.com/watch?v=S9zkuQmTDAY](https://www.youtube.com/watch?v=S9zkuQmTDAY)  
32. Help\! Focus stacking with Olympus : r/OlympusCamera \- Reddit, accessed May 5, 2026, [https://www.reddit.com/r/OlympusCamera/comments/1aepzh0/help\_focus\_stacking\_with\_olympus/](https://www.reddit.com/r/OlympusCamera/comments/1aepzh0/help_focus_stacking_with_olympus/)