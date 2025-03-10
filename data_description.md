The <strong>Hawkins</strong> experimental sequences feature scenes of dense forests and urban structures. The data were collected during the day with cloudy and windy conditions.
- Sequence 1-2: Features dense trees and branches with varying thickness.
- Sequence 3: Captures views of a thin pole, trees, and buildings representing typical urban obstacles that a UAS might face in response to a wildfire disaster.
- Sequence 4: Contains views of a car, pole, and distant trees.
- Sequence 5: replicated a disaster scenario of an upside-down car engulfed in dense smoke.

The <strong>Frick</strong> experimental sequences were recorded during the night and under rainy conditions. The captured temperature range for these sequences is much lower and is evident from the darker thermal images. These sequences feature bare trees in varying sparsity, vehicles, poles, roads and buildings.

<strong>Gascola</strong> sequences were recorded in heavily degraded wilderness, featuring dense smoke, night-time, dense trees and bushes. These conditions were chosen to simulate the wildfire disaster response scenario in which the UAS must navigate through a cluttered forest environment with extreme visual degradation. We show that depth estimation models trained on smokeless data are able to generalize to these smoke-filled data.

<strong>Firesgl</strong> sequences were recording during actual prescribed fires, capturing flames, embers, smoke, and dense trees. These sequences represent highly realistic wildfire scenarios, providing critical data for testing depth estimation in extreme environments.

<strong>Thermal</strong> are recorded in 16-bit raw for all collections besides Firesgl, which is logged in 8-bit RGB. Dataloader and visualization tool will be shared in our [github repo](https://github.com/firestereo/firestereo).

LiDAR and IMU <strong>rosbag</strong> files are provided for each Frick and Hawkins sequences:
- Frick: all topics in one bag
- Hawkins: topics in different bags
