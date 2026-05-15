# **Technical Optimization and Management of the OM System OM-1 Mark II Underwater Photographic Ecosystem**

The architecture of a high-end underwater imaging system requires a precise synchronization between sophisticated camera hardware, specialized housing ergonomics, and advanced lighting protocols. The OM System OM-1 Mark II represents the current zenith of Micro Four Thirds technology, offering substantial improvements in computational photography, autofocus reliability, and operational stability over its predecessors.1 For the professional underwater photographer, the integration of this body with the Nauticam NA-OM1 housing and the Backscatter Hybrid Flash ecosystem creates a versatile platform capable of addressing subjects ranging from super-macro nudibranchs to high-speed pelagic encounters. This report provides an exhaustive technical analysis of the system configurations, optical requirements, and strategic adjustments necessary to achieve peak performance in subaquatic environments.

## **Internal System Architecture and Sensor Dynamics**

The foundational strength of the OM-1 Mark II lies in its 20.4-megapixel quad-pixel AF stacked CMOS sensor, which works in tandem with the TruePic X processing engine.3 This hardware configuration facilitates a significant increase in data throughput, allowing for the rapid execution of the complex algorithms required for subject detection and computational image blending.5

### **Readout Speeds and Buffer Management**

Underwater photography often involves unpredictable, fast-moving subjects where shutter lag or buffer exhaustion can result in missed opportunities. The stacked sensor design reduces the time required for electronic readout, which effectively mitigates the rolling shutter effect when capturing rapid action or recording high-frame-rate video.2 The Mark II iteration has doubled the internal buffer size compared to the original OM-1, enabling the capture of up to 213 RAW frames at 120 frames per second (fps) in S-AF mode, or 256 RAW frames at 50 fps when using the SH2 sequential mode.4

| Sequential Shooting Mode | Max Frame Rate (fps) | Buffer Capacity (RAW) | AF/AE Tracking |
| :---- | :---- | :---- | :---- |
| SH1 (Electronic) | 120 | 213 4 | Locked at first frame 7 |
| SH2 (Electronic) | 50 | 256 6 | Yes (with compatible lenses) 4 |
| Silent Mode | 20 | 108 4 | Yes 7 |
| Mechanical Shutter | 10 | 139 4 | Yes 7 |

The capability to maintain 50 fps with continuous autofocus (C-AF) and exposure tracking is a critical differentiator for marine wildlife encounters.6 Lenses such as the M.Zuiko Digital ED 12-40mm F2.8 PRO II and the 40-150mm F2.8 PRO are specifically optimized to support these high-speed data exchanges.4

### **Sensitivity and Noise Suppression**

Light attenuation in the water column necessitates a sensor capable of maintaining high signal-to-noise ratios at elevated ISO settings. The native ISO range of the OM-1 Mark II extends to 102,400, though the standard default upper limit for Auto ISO is restricted to 25,600 to preserve image fidelity.4 Underwater, ISO 200 is considered the baseline for optimal dynamic range and minimal noise.9 The ability to pull the sensitivity down to ISO 80 (Low) allows the operator to use wider apertures or slower shutter speeds in shallow, bright conditions to better control ambient light and saturate background blues.4

## **Optical Integration and Port Logistics**

The refractive index of water creates a unique set of optical challenges, including magnification, chromatic aberration, and loss of edge sharpness. The Nauticam NA-OM1 housing addresses these through the N85 Port System, which allows for the mounting of dome and flat ports specifically engineered for Micro Four Thirds optics.5

### **Macro Optical Configurations**

The Micro Four Thirds format is exceptionally well-suited for macro photography due to its inherent 2x crop factor and the availability of world-class macro lenses. The M.Zuiko 60mm f/2.8 Macro remains the industry standard, offering a fast-focusing internal mechanism and compatibility with the Nauticam Macro Port 45\.12 For super-macro applications, the M.Zuiko 90mm f/3.5 Macro IS PRO provides 2:1 magnification natively, which can be further enhanced using external wet diopters like the Nauticam CMC or SMC series.3

| Lens | Recommended Port | Extension Ring | Application |
| :---- | :---- | :---- | :---- |
| 60mm f/2.8 Macro | Macro Port 45 12 | 20 12 | General Macro 14 |
| 90mm f/3.5 Macro IS PRO | Macro Port 45 | 30 or 40 | Super Macro / Skittish Critters 14 |
| 30mm f/3.5 Macro | Macro Port 45 12 | None 12 | Fish Portraits / Large Macro 12 |

The 90mm lens's longer focal length provides a greater working distance, which is essential when approaching skittish subjects like shrimp or gobies.14 This working distance prevents the housing from blocking strobe light and minimizes the risk of startling the subject.14

### **Wide-Angle and Water Contact Optics**

Wide-angle photography underwater requires minimizing the water-to-glass interface. Traditional dome ports correct for the magnification of water but can suffer from corner softness.12 The M.Zuiko 8mm f/1.8 PRO Fisheye is the premier choice for large reefs and wrecks, providing a 180-degree field of view that requires an N85 4.33” or larger acrylic dome port for optimal performance.12

A significant improvement in wide-angle versatility is achieved through Nauticam's Water Contact Optics, such as the WWL-1 (Wet Wide Lens). When paired with the M.Zuiko 14-42mm f/3.5-5.6 EZ lens, the WWL-1 provides a 130-degree field of view with full zoom-through capabilities, allowing the photographer to capture both wide scenes and close-up portraits on the same dive.5 This "Mission Control" approach to optics allows for greater flexibility in unpredictable environments.13

## **Ergonomic Command and Housing Dynamics**

The Nauticam NA-OM1 housing is not merely a waterproof container but an extension of the camera's interface, designed to facilitate intuitive operation while wearing gloves or managing buoyancy.2

### **Mission Control Design Philosophy**

Nauticam engineers have repositioned essential controls from the camera body to the housing's handles. The most critical integration is the thumb-actuated lever on the right handle that triggers the AF-ON button.2 This enables back-button autofocus, separating the focus command from the shutter release.17 This technique allows the photographer to lock focus on a subject and then wait for the exact moment of peak action or optimal composition without the camera attempting to refocus upon pressing the shutter.17

### **Vacuum Safety and Monitoring**

The housing features an integrated vacuum check and leak detection system as standard equipment.5 By installing the optional M14 Vacuum Valve II, the internal pressure can be reduced prior to the dive using a manual pump.5 A multi-color LED provides real-time status updates:

* **Flashing Orange/Yellow**: The system is analyzing the internal pressure or the vacuum is being established.18  
* **Constant Green**: The internal vacuum is stable, indicating a watertight seal.2  
* **Rapidly Flashing Red/Yellow**: Indicates a leak or pressure loss, signaling that the housing should not be submerged.19

This system is temperature-compensated to prevent false alarms caused by shifts in ambient temperature or internal camera heating.13

## **Advanced Autofocus and AI Subject Recognition**

The OM-1 Mark II utilizes a hybrid autofocus system with 1,053 cross-type phase-detection points, which provides comprehensive coverage across the entire sensor area.3 This architecture is particularly effective in low-light and low-contrast environments typical of underwater scenes.20

### **AI Subject Detection for Marine Life**

The "Intelligent Subject Detection AF" uses deep learning to identify and track specific subjects. While a dedicated "fish" mode is currently absent from Version 1.3 firmware, the "Bird" and "Animal" detection modes have proven highly effective for marine life.21 Field tests indicate that the "Bird" mode can reliably lock onto the eyes of fish, as the AI identifies the anatomical similarity between avian and ichthyic eye structures.22 This tracking remains effective even against busy backgrounds like coral reefs, where traditional AF systems might hunt.22

### **C-AF Sensitivity and Refinement**

For subjects moving through the water column, Continuous AF (C-AF) behavior must be tailored via the "AF Tab" in the camera menu.7

| AF Setting | Configuration Option | Implication for Underwater Use |
| :---- | :---- | :---- |
| C-AF Sensitivity | \+2 to \-2 | \+2 provides instant refocusing; \-2 ignores temporary obstructions like marine snow.23 |
| AF Target Mode | Single to All | Single point is best for macro eyes; All points are best for fast-moving pelagics.3 |
| AF Area Pointer | On1 or On2 | On2 provides cluster AF targeting, showing all active focus points during C-AF.7 |
| AF-ON in MF Mode | Yes | Allows for "Lock it and Rock it" focus techniques.17 |

The "Lock it and Rock it" technique is particularly useful in super-macro. The operator sets the lens to a specific magnification in Manual Focus (MF) and uses the AF-ON button to bring the subject into the general focal plane. Final razor-sharp focus is achieved by physically moving the housing slightly forward or backward while observing the focus peaking indicators.17

## **The Backscatter Hybrid Flash Ecosystem**

The Backscatter Hybrid Flash (HF-1) is a dual-purpose tool that combines a high-output strobe (Guide Number 40\) with a professional-grade 5,000-lumen video light.26 This integration is critical for modern hybrid shooters who require both high-speed flash for stills and constant light for video on a single dive.27

### **Digital Optical Smart Control (SC)**

The HF-1 utilizes a proprietary digital optical protocol known as Smart Control (SC) for automatic TTL exposure.28 Unlike traditional mimic TTL, which simply copies the duration of the camera's internal flash, Smart Control sends a computerized code through the fiber optic cable, providing the accuracy of a hardwired connection with the convenience of optical signaling.28

Two distinct TTL modes are provided:

1. **SC Mode**: Optimized for wide-angle and large-subject photography, such as turtles and reef scenes.7  
2. **SC Macro Mode**: Specifically calibrated for subjects eighteen inches and closer. This mode prevents the overexposure common in other TTL systems when shooting at extremely close ranges with wide apertures.28

### **High-Speed Sync and Super FP Protocols**

A significant limitation in underwater flash photography has traditionally been the camera's maximum sync speed, usually 1/250 second.7 The Hybrid Flash overcomes this using HSS (High-Speed Sync) or Super FP mode.7 By emitting a series of rapid micro-flashes, the strobe can synchronize with shutter speeds up to 1/8000 second.7 This allows the photographer to shoot wide-open (e.g., f/2.8) in shallow, sun-drenched water while maintaining a dark, controlled background, effectively "knocking down" the sun.27

### **Remote Lighting and Wireless Power Control**

The "REM" mode on the Hybrid Flash allows one "Main" strobe (connected via fiber optic to the camera) to wirelessly trigger and adjust the power levels of multiple "Remote" strobes.7 This is achieved using the included "Light Pipe," which captures the optical signal from the main strobe.7

| Remote Control Feature | Mechanism | Benefit |
| :---- | :---- | :---- |
| Power Adjustment | Test button pulse signals 7 | Change remote power without disturbing the subject.35 |
| Grouping | Group A, Channel 1 7 | Standardized communication across Backscatter flashes.34 |
| Confirmation | Confirmation flash 7 | Visual feedback that power setting was received.34 |
| Interference Block | Optional IR Filter 7 | Prevents the triggering strobe from appearing in the image.34 |

This system is cross-compatible with the Backscatter Mini Flash 2 and Mini Flash 3, allowing for complex multi-light setups on a single dive.34

## **Creative Lighting with the Optical Snoot OS-3**

The Optical Snoot OS-3, designed for the Hybrid Flash, is an essential accessory for isolating macro subjects.36 It projects a narrow, controlled beam of light that eliminates extraneous background detail and creates the highly sought-after "black background" effect.37

### **Aiming and Focus Light Integration**

One of the most challenging aspects of snooting is alignment. The HF-1 features a 1,500-lumen focus light that is perfectly aligned with the strobe's flash tube.35 This "what you see is what you get" implementation ensures that the flash hits exactly where the focus light is aimed, significantly increasing the hit rate for small, moving subjects.35 A red light mode is also integrated, which allows the photographer to aim at light-sensitive animals without inducing defensive behaviors.35

### **Diffusers and Color Temperature Manipulation**

The native color temperature of the Hybrid Flash is 6500K, which is slightly cooler than daylight.38 To manage the aesthetic qualities of the light, Backscatter provides a range of diffusers that modify the beam angle and spectral output.26

* **Standard White Diffuser**: Increases the beam angle to 140 degrees for general wide-angle use.7  
* **5500K Diffuser**: Corrects the color to a warmer, natural daylight hue, which is preferred for human model skin tones.7  
* **4500K Diffuser**: Designed for green-water environments; setting the camera's white balance to 4500K while using this diffuser turns the background water blue while maintaining accurate foreground colors.26  
* **Ambient Blue Diffuser**: Matches the color of the strobe to the surrounding water (optimal at depths of 10-35 feet). This allows the flash to fill shadows naturally without creating a "flash-lit" look with mixed color temperatures.7

## **Computational Photography in the Marine Environment**

The OM-1 Mark II leverages its high processing power to provide computational features that solve traditional underwater photographic problems in-camera.1

### **In-Camera Focus Stacking**

In macro photography, the depth of field is often limited to a few millimeters. The Focus Stacking mode captures between 3 and 15 shots at varying focus distances and composites them into a single image with an expanded depth of field.3

A technical constraint of this mode when using strobes is the 1/100 second shutter speed sync limit imposed by the electronic shutter.40 The camera will automatically override faster shutter speeds to 1/100s once stacking is engaged.40 Furthermore, the "Flash Charge Time" in the Focus Stacking menu must be set to 0.1 or 0.2 seconds to allow the Hybrid Flash to recycle between frames.25

### **Live GND (Graduated Neutral Density)**

The Live GND feature, exclusive to the Mark II body, is highly advantageous for split-shots (half-above, half-below water).6 It allows the operator to digitally darken the bright sky while leaving the darker underwater foreground properly exposed.41 The strength can be adjusted from GND2 to GND8, and the transition boundary can be rotated using the front and rear dials or the touchscreen.3

### **High Res Shot Modes**

The High Res Shot mode uses the sensor-shift mechanism to capture and combine multiple exposures. Handheld High Res produces a 50MP RAW file, while Tripod High Res produces an 80MP RAW file.3 The Mark II version introduces 14-bit RAW support for these modes, providing greater latitude for shadow recovery and color grading in post-processing.41 However, because this mode relies on multiple exposures, it is generally incompatible with flash and is best suited for stationary subjects under constant ambient or video light.4

## **Systematic Customization for Diving Efficiency**

The depth of the OM System menu (400-500 individual settings) requires a systematic approach to customization to ensure that the camera can be reconfigured instantly as environmental conditions change.42

### **My Menu Organization**

The "My Menu" tab should be utilized to aggregate frequently adjusted settings that lack a dedicated physical button or lever on the Nauticam housing.47 Recommended items for the primary page include:

1. **Card Slot Settings**: Critical for managing the dual SD slots (Overflow vs. Backup).7  
2. **Live View Boost**: Must be toggled "On" to ensure the monitor is visible in dark environments.9  
3. **Flash RC Mode**: Necessary for switching between manual triggering and Smart Control TTL.49  
4. **Subject Detection Toggle**: To quickly enable/disable AI tracking.51  
5. **Focus Stacking/Bracketing Settings**: To adjust the number of shots or differential on the fly.15

### **Nauticam Mission Control Button Mapping**

To maximize the ergonomic potential of the NA-OM1 housing, several buttons should be remapped from their default functions.5

* **Fn Lever (2x2 Switch)**: Configured to "Mode 2," this allows the front and rear dials to switch from controlling Aperture/Shutter Speed to controlling ISO/White Balance with a single flick.20  
* **Fn1 Button**: Recommended for "One-Touch White Balance" or "AEL Focus Lock".9  
* **Fn2 Button**: Recommended for toggling "Manual Focus" (MF), allowing the photographer to quickly take control if the AF hunts.9  
* **Trash/Erase Button**: Can be re-mapped via the latest firmware to serve as a menu access shortcut, allowing all key navigation to be performed with the right hand.21

## **Maintenance, Reliability, and Firmware Management**

The high-end nature of the OM-1 Mark II and its accessories demands strict maintenance protocols to prevent equipment failure in harsh marine environments.

### **Power Management and the 21700 Ecosystem**

The Backscatter Hybrid Flash relies on high-performance 21700 lithium-ion batteries.27 It is critical to use "protected" cells that include electronic circuits to prevent overcharge, short circuits, and extreme temperature fluctuations.7 Unprotected cells, often identified by the lack of branding or a plain colored jacket, pose a significant fire and explosion risk.7 The flash requires a high continuous current draw (25A or 20A) to support its Guideline Number 40 output and rapid recycle times.7

| Strobe Output | Recycle Time (seconds) | Flashes per Charge (approx.) |
| :---- | :---- | :---- |
| GN 40 (Boost \+2) | 1.6 \- 2.17 | 375+ 7 |
| GN 34 (Boost \+1) | 0.7 \- 1.17 | 800+ 7 |
| GN 29 (Full) | 0.5 \- 0.86 | 1,000+ 7 |

### **O-Ring Integrity and Triple-Layer Protection**

The Hybrid Flash uses three layers of protection for its battery compartment: two main body O-rings and a sand seal gasket.7 The sand seal is a non-watertight gasket designed to keep debris away from the primary seals.7 Operators must never apply grease to the sand seal, as this will attract particulate matter that could migrate to the O-rings and cause a compromise.7 Only the manufacturer-provided silicone grease should be used on the main O-rings; petroleum-based lubricants (like WD-40) will cause massive swelling and permanent material failure.7

### **Thermal Management and Safety Protocols**

High-power strobes generate significant internal heat during rapid-fire sequences.26 The Hybrid Flash includes an aluminum head and multiple internal sensors to manage this.26 If the overheating threshold is reached—typically after 35-55 rapid full-power shots—the flash emits a long beep and flashes a purple light.7 It will then automatically reduce its power output by 1/2 stop to continue shooting while cooling down.7 If firing continues in this state, a mandatory 2-minute cooldown period will be enforced.7

### **Firmware Update Procedures**

Ensuring the OM-1 Mark II and its lenses are running the most recent firmware is vital for autofocus accuracy and operational stability.32 Updates can be performed via the OI.Share mobile app or the OM Workspace desktop application.32

| Firmware Version | Major Improvements / Features |
| :---- | :---- |
| Version 1.1 | Smartphone connection security (WPA2); functional stability.21 |
| Version 1.2 | Enhanced Handheld High-Res composition algorithm; stability improvements.21 |
| Version 1.3 | Improved touch panel stability during playback.21 |

During the update process, the camera must have a fully charged battery, and the USB cable must not be disconnected until the LCD displays "OK".21 A power interruption during firmware writing can result in the camera becoming inoperable and requiring factory service.21

## **Systematic Buoyancy and Rig Balancing**

A professional underwater rig is often heavy in air but must be neutral or slightly negative in water to prevent wrist fatigue and ensure stable shooting platforms.

### **Buoyancy Compensation Tools**

The Nauticam NA-OM1, with a camera and battery installed, is approximately \-0.2 kg in water, but the addition of strobes, arms, and ports can significantly increase this weight.2 Buoyancy can be managed through several methods:

1. **Carbon Fiber Float Arms**: These provide inherent buoyancy to offset the weight of the strobes and clamps.45  
2. **Stix Floats**: High-density foam floats that can be added to standard aluminum arms to fine-tune the rig's balance.45  
3. **Handle Brackets**: Stainless steel handle brackets on the NA-OM1 provide rigidity and additional mounting points for focus lights or lanyards.13

Achieving a neutral balance allows the photographer to release the rig if necessary to manage dive tasks without the camera sinking or floating away, and it provides the stability required for the 8.5 stops of IBIS to work effectively in handheld macro video capture.20

## **Practical Tactical Insights for Professional Use**

The successful deployment of the OM-1 Mark II system depends on the operator’s ability to transition from technical understanding to tactical execution.

The causal relationship between the quad-pixel AF system and the Hybrid Flash's high-speed recycling enables a "machine gun" approach to macro photography that was previously impossible. By utilizing SH2 mode at 20 or 50 fps with the strobe at 1/8 power, an operator can capture a high-speed behavior—such as a goby jumping—with dozens of perfectly exposed and focused frames to choose from.38

The integration of computational modes like Live GND for split-shots provides a significant advantage in travel photography, where reducing the need for physical filters simplifies the rig and decreases the risk of damage or loss.41 Furthermore, the ability to perform 2:1 super-macro with the 90mm lens without an external dioptric change allows for a faster response to different subject sizes encountered on a single dive.14

The complexity of the system is mitigated by the "Mission Control" ergonomics of the Nauticam housing and the "Smart Control" logic of the Backscatter lighting. By pre-setting Custom Modes C1-C4, the photographer can remain mentally engaged with the environment and the subject, trusting that the technical foundations of the shot—exposure, focus, and lighting—are pre-configured and ready for immediate activation. This synergy between stabilization, speed, and intelligent lighting confirms the OM System OM-1 Mark II ecosystem as a premier solution for the modern professional underwater image-maker.

#### **Works cited**

1. OM-1 MkII announced \- Photography Gear and Technique \- WaterPixels, accessed May 4, 2026, [https://waterpixels.net/forums/topic/813-om-1-mkii-announced/](https://waterpixels.net/forums/topic/813-om-1-mkii-announced/)  
2. OM-Systems OM-1 (II) Underwater Housing by Nauticam \- PanOceanPhoto, accessed May 4, 2026, [https://panoceanphoto.com/en/Nauticam-OM-Systems-OM-1](https://panoceanphoto.com/en/Nauticam-OM-Systems-OM-1)  
3. Explore OM-1 Mark II Camera From OM SYSTEM, accessed May 4, 2026, [https://explore.omsystem.com/us/en/om-1-mark-ii](https://explore.omsystem.com/us/en/om-1-mark-ii)  
4. OM System OM-1 II Mirrorless Camera Body \- Backscatter.com, accessed May 4, 2026, [https://www.backscatter.com/OM-System-OM-1-II-Mirrorless-Camera-Body](https://www.backscatter.com/OM-System-OM-1-II-Mirrorless-Camera-Body)  
5. NA-OM1 Housing for OM System OM-1 and OM-1 Mark II Camera \- Nauticam, accessed May 4, 2026, [https://www.nauticam.com/products/na-om1-housing-for-olympus-om-1-camera](https://www.nauticam.com/products/na-om1-housing-for-olympus-om-1-camera)  
6. OM-1 Mark II \- OM System \- Olympus, accessed May 4, 2026, [https://explore.omsystem.com/c/en/om-1-mark-ii](https://explore.omsystem.com/c/en/om-1-mark-ii)  
7. OM-1\_Mark\_II\_MANUAL\_EN.pdf  
8. OM SYSTEM OM-1 Mark II User's Guide \- Ken Rockwell, accessed May 4, 2026, [https://www.kenrockwell.com/om/om-1-ii-users-guide.htm](https://www.kenrockwell.com/om/om-1-ii-users-guide.htm)  
9. Best Underwater Settings for the Olympus OM-D E-M1 Mark II Camera, accessed May 4, 2026, [https://www.uwphotographyguide.com/olympus-omd-em1-markii-best-underwater-settings/](https://www.uwphotographyguide.com/olympus-omd-em1-markii-best-underwater-settings/)  
10. My OM-1: Custom Settings for Field Macro \- OM SYSTEM LEARN CENTER, accessed May 4, 2026, [https://learnandsupport.getolympus.com/learn-center/photography-tips/macro/my-om-1-custom-settings-for-field-macro](https://learnandsupport.getolympus.com/learn-center/photography-tips/macro/my-om-1-custom-settings-for-field-macro)  
11. Nauticam OM System OM-1 I & II Underwater Housing NA-OM1 \- Backscatter.com, accessed May 4, 2026, [https://www.backscatter.com/Nauticam-Olympus-OM-1-Underwater-Housing-NA-OM1](https://www.backscatter.com/Nauticam-Olympus-OM-1-Underwater-Housing-NA-OM1)  
12. My OM-1 Underwater Photography Rig — Brian G Weber Photography, accessed May 4, 2026, [https://blog.briangweber.com/om1-photo-rig](https://blog.briangweber.com/om1-photo-rig)  
13. Nauticam OM System OM-1 OM-1 II Underwater Housing., accessed May 4, 2026, [https://www.bluewaterphotostore.com/nauticam-olympus-om1-housing](https://www.bluewaterphotostore.com/nauticam-olympus-om1-housing)  
14. OM System OM-1 II Underwater Camera Review \- GEAR TESTS ..., accessed May 4, 2026, [https://www.thedigitalshootout.com/little-cayman-2024/gear-tests/om-system-om-1-ii-underwater-camera-review-gear-tests-event-coverage-2024-little-cayman/](https://www.thedigitalshootout.com/little-cayman-2024/gear-tests/om-system-om-1-ii-underwater-camera-review-gear-tests-event-coverage-2024-little-cayman/)  
15. Embarking on a Macro Photography Journey with the OM-1 Mark II, accessed May 4, 2026, [https://learnandsupport.getolympus.com/learn-center/photography-tips/macro/embarking-on-a-macro-photography-journey-with-the-om-1-mark-ii](https://learnandsupport.getolympus.com/learn-center/photography-tips/macro/embarking-on-a-macro-photography-journey-with-the-om-1-mark-ii)  
16. Dive Into Underwater Photography \- OM SYSTEM LEARN CENTER, accessed May 4, 2026, [https://learnandsupport.getolympus.com/learn-center/photography-tips/underwater/dive-into-underwater-photography](https://learnandsupport.getolympus.com/learn-center/photography-tips/underwater/dive-into-underwater-photography)  
17. Back Button Focus \- Nauticam, accessed May 4, 2026, [https://www.nauticam.com/blogs/news/back-button-focus](https://www.nauticam.com/blogs/news/back-button-focus)  
18. general guide aoi uh-om1 underwater housing, accessed May 4, 2026, [https://www.aoi-uw.com/media/wysiwyg/AOI\_UH-OM1\_General\_Guide.pdf](https://www.aoi-uw.com/media/wysiwyg/AOI_UH-OM1_General_Guide.pdf)  
19. 17819 NA-OM1 Product Manual.indd \- PanOceanPhoto, accessed May 4, 2026, [https://panoceanphoto.com/mediafiles/pdfs/NA17819\_OM-Systems-OM1-Bedienungsanleitung-Nauticam-en.pdf](https://panoceanphoto.com/mediafiles/pdfs/NA17819_OM-Systems-OM1-Bedienungsanleitung-Nauticam-en.pdf)  
20. Olympus OM-D E-M1 Mark II Underwater Camera Review \- Backscatter.com, accessed May 4, 2026, [https://www.backscatter.com/reviews/post/Olympus-OM-D-E-M1-MarkII-Underwater-Camera-Review](https://www.backscatter.com/reviews/post/Olympus-OM-D-E-M1-MarkII-Underwater-Camera-Review)  
21. firmware | OM SYSTEM Norway \- OM System \- Olympus, accessed May 4, 2026, [https://explore.omsystem.com/no/en/firmware](https://explore.omsystem.com/no/en/firmware)  
22. OM-1 mki vs Oly EM-10 mk iv autofocus on moving fish? \- WaterPixels, accessed May 4, 2026, [https://waterpixels.net/forums/topic/1568-om-1-mki-vs-oly-em-10-mk-iv-autofocus-on-moving-fish/](https://waterpixels.net/forums/topic/1568-om-1-mki-vs-oly-em-10-mk-iv-autofocus-on-moving-fish/)  
23. OM-1 & OM-1 Mark II Settings: AF Settings \- YouTube, accessed May 4, 2026, [https://www.youtube.com/watch?v=ihDKqa9o6P0](https://www.youtube.com/watch?v=ihDKqa9o6P0)  
24. Optimal Bird and Wildlife Settings for OM-1 & OM-1 MKII: A Comparison of Rob Trek and Steven Ingram's Techniques \- Open Source Photography, accessed May 4, 2026, [https://marcrphoto.wordpress.com/2024/07/01/optimal-bird-and-wildlife-settings-for-om-1-om-1-mkii-a-comparison-of-rob-trek-and-steven-ingrams-techniques/](https://marcrphoto.wordpress.com/2024/07/01/optimal-bird-and-wildlife-settings-for-om-1-om-1-mkii-a-comparison-of-rob-trek-and-steven-ingrams-techniques/)  
25. My OM-1: Custom Settings for Field Macro \- OM SYSTEM LEARN CENTER, accessed May 4, 2026, [https://learnandsupport.getolympus.com/ca-en/learn-center/photography-tips/macro/my-om-1-custom-settings-for-field-macro](https://learnandsupport.getolympus.com/ca-en/learn-center/photography-tips/macro/my-om-1-custom-settings-for-field-macro)  
26. Backscatter Hybrid Flash Underwater Strobe & Video Light HF-1, accessed May 4, 2026, [https://www.backscatter.com/Backscatter-Hybrid-Flash-Underwater-Strobe-Video-Light-HF-1](https://www.backscatter.com/Backscatter-Hybrid-Flash-Underwater-Strobe-Video-Light-HF-1)  
27. Backscatter Hybrid Flash Single Underwater Strobe & Ultralight Arm Package, accessed May 4, 2026, [https://www.backscatter.com/Backscatter-Hybrid-Flash-Single-Underwater-Strobe-Ultralight-Arm-Package](https://www.backscatter.com/Backscatter-Hybrid-Flash-Single-Underwater-Strobe-Ultralight-Arm-Package)  
28. Backscatter Smart Control TTL LED Universal Flash Trigger for Sony, accessed May 4, 2026, [https://www.backscatter.com/Backscatter-Smart-Control-TTL-LED-Universal-Flash-Trigger-for-Sony](https://www.backscatter.com/Backscatter-Smart-Control-TTL-LED-Universal-Flash-Trigger-for-Sony)  
29. Backscatter Smart Control TTL LED Universal Flash Trigger for OM System & Olympus, accessed May 4, 2026, [https://www.backscatter.com/Backscatter-Smart-Control-TTL-LED-Universal-Flash-Trigger-for-OM-System-Olympus](https://www.backscatter.com/Backscatter-Smart-Control-TTL-LED-Universal-Flash-Trigger-for-OM-System-Olympus)  
30. Backscatter TTL Flash Trigger Review \- The Underwater Club, accessed May 4, 2026, [https://theunderwaterclub.com/blog/backscatter-ttl-flash-trigger-review/](https://theunderwaterclub.com/blog/backscatter-ttl-flash-trigger-review/)  
31. MF-2-Instructions.pdf \- Backscatter.com, accessed May 4, 2026, [https://www.backscatter.com/images/article/content/Mini-Flash-2/MF-2-Instructions.pdf](https://www.backscatter.com/images/article/content/Mini-Flash-2/MF-2-Instructions.pdf)  
32. Firmware update instructions \- OM System \- Olympus, accessed May 4, 2026, [https://explore.omsystem.com/us/en/firmware-update-instructions](https://explore.omsystem.com/us/en/firmware-update-instructions)  
33. OM-1 & OM-1 Mark II: Focus Stacking Explained with Chris McGinnis \- YouTube, accessed May 4, 2026, [https://www.youtube.com/watch?v=7li\_p6zXqhQ](https://www.youtube.com/watch?v=7li_p6zXqhQ)  
34. Remote Lighting with Backscatter Hybrid Flash, Atom Flash, Mini ..., accessed May 4, 2026, [https://www.backscatter.com/reviews/post/Remote-Lighting-with-Backscatter-Hybrid-Flash-Mini-Flash-2-Underwater-Guide](https://www.backscatter.com/reviews/post/Remote-Lighting-with-Backscatter-Hybrid-Flash-Mini-Flash-2-Underwater-Guide)  
35. Backscatter Hybrid Flash Underwater Optical Snoot Review, accessed May 4, 2026, [https://www.backscatter.com/reviews/post/Backscatter-Hybrid-Flash-Underwater-OS-3-Snoot-Review](https://www.backscatter.com/reviews/post/Backscatter-Hybrid-Flash-Underwater-OS-3-Snoot-Review)  
36. Backscatter \- Hybrid Flash & Optical Snoot Combo Package \- Paragon Dive Group, accessed May 4, 2026, [https://www.paragondivestore.com/products/backscatter-hybrid-flash-optical-snoot-combo-package](https://www.paragondivestore.com/products/backscatter-hybrid-flash-optical-snoot-combo-package)  
37. Snoot Photography Made Easy: Backscatter MF-01 & OS-01 | Lembeh Resort, accessed May 4, 2026, [https://www.lembehresort.com/blogs/snoot-photography-backscatter](https://www.lembehresort.com/blogs/snoot-photography-backscatter)  
38. Backscatter Hybrid Flash Final Review \- The Underwater Club, accessed May 4, 2026, [https://theunderwaterclub.com/blog/backscatter-hybrid-flash-final-review/](https://theunderwaterclub.com/blog/backscatter-hybrid-flash-final-review/)  
39. Backscatter Hybrid Flash Underwater Strobe & Video Light Review, accessed May 4, 2026, [https://www.backscatter.com/reviews/post/Backscatter-Hybrid-Flash-Underwater-Strobe-Video-Light-Review](https://www.backscatter.com/reviews/post/Backscatter-Hybrid-Flash-Underwater-Strobe-Video-Light-Review)  
40. How to setup your OM SYSTEM camera for focus bracketing and focus stacking \- wildmacro, accessed May 4, 2026, [https://wildmacro.de/how-to-setup-your-om-system-camera-for-focus-bracketing-and-focus-stacking/](https://wildmacro.de/how-to-setup-your-om-system-camera-for-focus-bracketing-and-focus-stacking/)  
41. OM system OM-1 II – first impression | Petr Bambousek | Wildlife Photography, accessed May 4, 2026, [https://www.sulasula.com/en/om-system-om-1-ii-first-impression/](https://www.sulasula.com/en/om-system-om-1-ii-first-impression/)  
42. Giant OM1 I and II spreadsheets of my top photo settings, accessed May 4, 2026, [https://mcaughtry.photo/giant-om1-i-and-ii-spreadsheets/](https://mcaughtry.photo/giant-om1-i-and-ii-spreadsheets/)  
43. Saving Custom Settings to the Mode Dial (C1, C2, C3, and C4 Custom Modes), accessed May 4, 2026, [https://learning.omsystem.com/OM-1MarkII/zz\_html\_manual/en/taking\_pictures\_using\_c\_26.html](https://learning.omsystem.com/OM-1MarkII/zz_html_manual/en/taking_pictures_using_c_26.html)  
44. My OM-1: Custom Settings for Field Macro \- OM SYSTEM LEARN CENTER, accessed May 4, 2026, [https://learnandsupport.getolympus.com/la-es/node/2284](https://learnandsupport.getolympus.com/la-es/node/2284)  
45. Guide to shooting Underwater with the Olympus OM-D E-M1 \- Bluewater Photo, accessed May 4, 2026, [https://www.bluewaterphotostore.com/guide-shooting-olympus-om-d-e-m1](https://www.bluewaterphotostore.com/guide-shooting-olympus-om-d-e-m1)  
46. New Om-1ii owner. What's on your C1-C4? : r/M43 \- Reddit, accessed May 4, 2026, [https://www.reddit.com/r/M43/comments/1l2vg88/new\_om1ii\_owner\_whats\_on\_your\_c1c4/](https://www.reddit.com/r/M43/comments/1l2vg88/new_om1ii_owner_whats_on_your_c1c4/)  
47. OM-1 My Menu Setup | Quick Tutorial \- YouTube, accessed May 4, 2026, [https://www.youtube.com/watch?v=ao1loa9Wee4](https://www.youtube.com/watch?v=ao1loa9Wee4)  
48. OM-System OM1-MKII Guide \- \- Phil Norton Photography, accessed May 4, 2026, [https://www.philnortonphotographyblog.co.uk/om-system-om1-mk2-guide](https://www.philnortonphotographyblog.co.uk/om-system-om1-mk2-guide)  
49. Wireless Remote Flash Control (A RC Mode) \- Camera How To, accessed May 4, 2026, [https://learning.omsystem.com/OM-1MarkII/zz\_html\_manual/en/flash\_rc\_mode\_105.html](https://learning.omsystem.com/OM-1MarkII/zz_html_manual/en/flash_rc_mode_105.html)  
50. ttl flash trigger for om system & olympus cameras universal \- Backscatter.com, accessed May 4, 2026, [https://www.backscatter.com/images/article/content/Backscatter-TTL-Flash-Trigger/bs-tr-om1-Manual.pdf](https://www.backscatter.com/images/article/content/Backscatter-TTL-Flash-Trigger/bs-tr-om1-Manual.pdf)  
51. OM-1 & OM-1 Mark II: AI Detection AF \- YouTube, accessed May 4, 2026, [https://www.youtube.com/watch?v=soIZWY0N3Og](https://www.youtube.com/watch?v=soIZWY0N3Og)  
52. How to properly configure OM-1 Mark II for bird detection? : r/M43 \- Reddit, accessed May 4, 2026, [https://www.reddit.com/r/M43/comments/1pvcxcm/how\_to\_properly\_configure\_om1\_mark\_ii\_for\_bird/](https://www.reddit.com/r/M43/comments/1pvcxcm/how_to_properly_configure_om1_mark_ii_for_bird/)  
53. OM-1 & OM-1 Mark II Settings: Focus stacking \- YouTube, accessed May 4, 2026, [https://www.youtube.com/watch?v=c5qxPdUTVjQ](https://www.youtube.com/watch?v=c5qxPdUTVjQ)  
54. Customizing the Fn Lever (Fn Lever Settings) \- Camera How To, accessed May 4, 2026, [https://learning.omsystem.com/OM-1MarkII/zz\_html\_manual/en/fn\_lever\_settings\_205.html](https://learning.omsystem.com/OM-1MarkII/zz_html_manual/en/fn_lever_settings_205.html)  
55. Latest Firmware Updates for Your OM System Cameras Improve Stability and Performance, accessed May 4, 2026, [https://nofilmschool.com/om-system-camera-firmware-updates](https://nofilmschool.com/om-system-camera-firmware-updates)  
56. Backscatter Hybrid FLash Instruction Manual, accessed May 4, 2026, [https://www.backscatter.com/images/article/content/Hybrid-Flash/Backscatter-Hybrid-Flash-Instruction-Manual.pdf](https://www.backscatter.com/images/article/content/Hybrid-Flash/Backscatter-Hybrid-Flash-Instruction-Manual.pdf)  
57. Joint update service for Interchangeable Lens Cameras \- OM Digital Solutions, accessed May 4, 2026, [https://support.jp.omsystem.com/en/support/imsg/digicamera/download/software/firm/e1/](https://support.jp.omsystem.com/en/support/imsg/digicamera/download/software/firm/e1/)  
58. OM SYSTEM OM-1, accessed May 4, 2026, [https://learnandsupport.getolympus.com/support/om-system-om-1](https://learnandsupport.getolympus.com/support/om-system-om-1)  
59. OM SYSTEM OM-1 Mark II, accessed May 4, 2026, [https://learnandsupport.getolympus.com/ca-en/support/om-system-om-1-mark-ii](https://learnandsupport.getolympus.com/ca-en/support/om-system-om-1-mark-ii)  
60. OM System released firmware updates for the OM-1 Mark II and OM-3 cameras \- 43addict, accessed May 4, 2026, [https://43addict.com/2025/07/01/om-system-released-firmware-updates-for-the-om-1-mark-ii-and-om-3-cameras/](https://43addict.com/2025/07/01/om-system-released-firmware-updates-for-the-om-1-mark-ii-and-om-3-cameras/)