using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TileSets : MonoBehaviour {

    public enum eForestTiles
    {
        //Layer 0 left empty for map background options
        //Layer 1
        Dirt = 1,
        //Layer 2
        Grass = 1 << 1,
        //Layer 3
        Tree = 1 << 2 | Grass,
        Rock = 1 << 3 | Dirt,
        Boulder = 1 << 4 | Dirt
    }

    public enum eCaveTiles
    {
        //Layer 0 left empty for map background options
        //Layer 1
        Dirt = 1
        //Layer 2


    }
}
