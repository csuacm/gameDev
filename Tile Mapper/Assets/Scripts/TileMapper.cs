using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;

public class TileMapper : MonoBehaviour {


    public const int height = 50;
    public const int width = 80;

    int[,] generatedMap = new int[height, width];

    public enum eMapStyle { Forest, Cave, Desert};

    //------------------------------------------------------------------------------------------------------------------------------------------------------------------
    //Takes the Style of the map and makes a map based on that style
    //Also takes a 4 bit number to add gates to the map(WestSouthEastNorth)
    //TODO: Make more paramaters to define the maps uniqueness
    void GenerateMap(eMapStyle mapStyle, int bitGates)
    {

        switch (mapStyle)
        {
            case eMapStyle.Forest:
                //Make the map blocks
                for (int i = 0; i < height; ++i)
                {
                    for (int j = 0; j < width; ++j)
                    {
                        generatedMap[i, j] = 0;
                    }
                }
                //Add path gates
                if (bitGates == 0)
                {
                    Debug.Log("Must have a gate!");
                    return;
                }

                int mask = 1;
                int[] northGate = new int[2];
                int[] eastGate = new int[2];
                int[] southGate = new int[2];
                int[] westGate = new int[2];
                //Make a random mid point

                int[] mid = new int[2];
                mid[0] = (height / 2) + Random.Range(-(height/3), (height / 3));
                mid[1] = (width / 2) + Random.Range(-(height / 3), (height / 3));

                for (int i = 0; i < 4; ++i)
                {
                    

                    generatedMap[mid[0], mid[1]] = 2;

                    if((mask & bitGates) != 0)
                    {
                        int randomNumber;
                        switch (i)
                        {
                            case 0://North
                                randomNumber = Random.Range(1, width - 2);
                                generatedMap[0, randomNumber] = 1;
                                northGate[0] = 0;
                                northGate[1] = randomNumber;
                                ConnectGate(northGate, mid);
                                break;
                            case 1://East
                                randomNumber = Random.Range(1, height - 2);
                                generatedMap[randomNumber, width - 1] = 1;
                                eastGate[0] = randomNumber;
                                eastGate[1] = width - 1;
                                ConnectGate(eastGate, mid);
                                break;
                            case 2://South
                                randomNumber = Random.Range(1, width - 2);
                                generatedMap[height - 1, randomNumber] = 1;
                                southGate[0] = height - 1;
                                southGate[1] = randomNumber;
                                ConnectGate(southGate, mid);
                                break;
                            case 3://West
                                randomNumber = Random.Range(1, height - 2);
                                generatedMap[randomNumber, 0] = 1;
                                westGate[0] = randomNumber;
                                westGate[1] = 0;
                                ConnectGate(westGate, mid);
                                break;
                        }
                    }
                    mask <<= 1;
                }
                


                break;
            case eMapStyle.Cave:

                break;
            case eMapStyle.Desert:

                break;
        }
    }

    struct Box
    {
        public int low;
        public int high;
        public Box(int l, int h)
        {
            low = l;
            high = h;
        }
    }

    void ConnectGate(int[] start, int[] end)
    {

        bool connected = false;
        Box[,] move = new Box[3, 3];
        while (!connected)
        {
            //update move
            int R = start[0] - end[0];
            int C = start[1] - end[1];
            //clear past move
            for(int i = 0; i < 3; i++)
            {
                for(int j = 0; j < 3; j++)
                {
                    Box b = new Box(0, 0);
                    move[i, j] = b;
                }
            }

            //RANGE VALUES------------------------------------------------------------------------------------------
            int highChance = 14;
            int midChanceLow = 15;
            int midChanceHigh = 16;
            int midChanceLow1 = 17;
            int midChanceHigh1 = 18;
            int lowChance = 19;
            int lowChance1 = 20;
            //set potenial moves
            if (R < 0)//Below
            {
                if (C == 0)//same col 
                {
                    move[2, 1].high = highChance;//D
                    move[2, 0].low = midChanceLow; move[2, 0].high = midChanceHigh;//DL
                    move[2, 2].low = midChanceLow1; move[2, 2].high = midChanceHigh1;//DR
                    move[1, 0].low = 19; move[1, 0].high = 19;//L
                    move[1, 2].low = 20; move[1, 2].low = 20;//R
                }
                else if (C > 0)//down left
                {
                    move[2, 0].high = highChance;//DL
                    move[2, 1].low = midChanceLow; move[2, 1].high = midChanceHigh;//D
                    move[1, 0].low = midChanceLow1; move[1, 0].high = midChanceHigh1;//L
                    move[0, 0].low = lowChance; move[0, 0].high = lowChance;//UL
                    move[2, 2].low = 20; move[2, 2].high = 20;//DR
                }
                else//down right
                {
                    move[2, 2].high = highChance;//DR
                    move[2, 1].low = midChanceLow; move[2, 1].high = midChanceHigh;//D
                    move[1, 2].low = midChanceLow1; move[1, 2].high = midChanceHigh1;//R
                    move[2, 0].low = lowChance; move[2, 0].high = lowChance;//DL
                    move[0, 2].low = lowChance1; move[0, 2].high = lowChance1;//UR
                }
            }
            else if(R > 0)//Above
            {
                if (C == 0)//same col 
                {
                    move[0, 1].high = highChance;//U
                    move[0, 0].low = midChanceLow; move[0, 0].high = midChanceHigh;//UL
                    move[0, 2].low = midChanceLow1; move[0, 2].high = midChanceHigh1;//UR
                    move[1, 0].low = lowChance; move[1, 0].high = lowChance;//L
                    move[1, 2].low = lowChance1; move[1, 2].high = lowChance1;//R
                }
                else if (C > 0)//up left
                {
                    move[0, 0].high = highChance;//UL
                    move[0, 1].low = midChanceLow; move[0, 1].high = midChanceHigh;//U
                    move[1, 0].low = midChanceLow1; move[1, 0].high = midChanceHigh1;//L
                    move[2, 0].low = lowChance; move[2, 0].high = lowChance;//DL
                    move[0, 2].low = lowChance1; move[0, 2].high = lowChance1;//UR
                }
                else//up right
                {
                    move[0, 2].high = highChance;//UR
                    move[0, 1].low = midChanceLow; move[0, 1].high = midChanceHigh;//U
                    move[1, 2].low = midChanceLow1; move[1, 2].high = midChanceHigh1;//R
                    move[0, 0].low = lowChance; move[0, 0].high = lowChance;//UL
                    move[2, 2].low = lowChance1; move[2, 2].high = lowChance1;//DR
                }
            }
            else//R == 0
            {
                if(C > 0)//Left
                {
                    move[1, 0].high = highChance;//L
                    move[0, 0].low = midChanceLow; move[0, 0].high = midChanceHigh;//UL
                    move[2, 0].low = midChanceLow1; move[2, 0].high = midChanceHigh1;//DL
                    move[0, 1].low = lowChance; move[0, 1].high = lowChance;//U
                    move[2, 1].low = lowChance1; move[2, 1].high = lowChance1;//D
                }
                else//Right
                {
                    move[1, 2].low = highChance;//R
                    move[0, 2].low = midChanceLow; move[0, 2].high = midChanceHigh;//UR
                    move[2, 2].low = midChanceLow1; move[2, 2].high = midChanceHigh1;//DR
                    move[0, 1].low = lowChance; move[0, 1].high = lowChance;//U
                    move[2, 1].low = lowChance1; move[2, 1].high = lowChance1;//D
                }
            }
            //check validity of move
            if(start[0] == 0 || start[0] == (height - 1))//no horizontal 
            {
                move[1, 0].low = 0; move[1, 0].high = 0;//L
                move[1, 2].low = 0; move[1, 2].high = 0;//R
                if(start[0] == 0)
                {
                    move[0, 0].low = 0; move[0, 0].high = 0;//UL
                    move[0, 2].low = 0; move[0, 2].high = 0;//UR
                }
                else
                {
                    move[2, 0].low = 0; move[2, 0].high = 0;//DL
                    move[2, 2].low = 0; move[2, 2].high = 0;//DR
                }
                
            }
            if (start[1] == 0 || start[1] == (width - 1))//no vertical
            {
                move[0, 1].low = 0; move[0, 1].high = 0;//U
                move[2, 1].low = 0; move[2, 1].high = 0;//D
                if (start[1] == 0)
                {
                    move[0, 0].low = 0; move[0, 0].high = 0;//UL
                    move[2, 0].low = 0; move[2, 0].high = 0;//DL
                }
                else
                {
                    move[0, 2].low = 0; move[0, 2].high = 0;//UR
                    move[2, 2].low = 0; move[2, 2].high = 0;//DR
                }
            }
            if (start[0] == 1)//near top then no up movement
            {
                move[0, 0].low = 0; move[0, 0].high = 0; //UL
                move[0, 1].low = 0; move[0, 1].high = 0; //U
                move[0, 2].low = 0; move[0, 2].high = 0; //UR
            }
            if(start[0] == height - 2)//near bottom then no down
            {
                move[2, 0].low = 0; move[2, 0].high = 0; //DL
                move[2, 1].low = 0; move[2, 1].high = 0; //D
                move[2, 2].low = 0; move[2, 2].high = 0; //DR
            }
            if(start[1] == 1)//near left then no left
            {
                move[0, 0].low = 0; move[0, 0].high = 0;//UL
                move[1, 0].low = 0; move[1, 0].high = 0;//L
                move[2, 0].low = 0; move[2, 0].high = 0;//DL
            }
            if(start[1] == width - 2)//near right then no right
            {
                move[0, 2].low = 0; move[0, 2].high = 0;//UR
                move[1, 2].low = 0; move[1, 2].high = 0;//R
                move[2, 2].low = 0; move[2, 2].high = 0;//DR
            }

            //make move
            bool moveMade = false;
            while (!moveMade)
            {
                int moveNumber = Random.Range(1, 21);
                for(int i = 0; i < 3; i++)
                {
                    for(int j = 0; j < 3; j++)
                    {
                        if (move[i, j].low <= moveNumber && move[i, j].high >= moveNumber)
                        {
                            if (generatedMap[start[0] + i - 1, start[1] + j - 1] != 1)
                            {
                                start[0] += i - 1;
                                start[1] += j - 1;
                                generatedMap[start[0], start[1]]++;
                                moveMade = true;
                                break;
                            }

                        }
                        
                    }
                }
                
            }

            //check if end is reached
            
            if (Mathf.Abs(start[0] - end[0]) == 1 || Mathf.Abs(start[0] - end[0]) == 0)
            {
                if (Mathf.Abs(start[1] - end[1]) == 1)
                    connected = true;
            }
                
            if (Mathf.Abs(start[1] - end[1]) == 1 || Mathf.Abs(start[1] - end[1]) == 0)
            {
                if (Mathf.Abs(start[0] - end[0]) == 1)
                    connected = true;
            }
                
        }
    }


    //Store the map in a text file, so that the visited map will persist
    void StoreMap()
    {
        var streamWriter = new StreamWriter(@"C:\Users\cwlarson\OneDrive\Tile Mapper\Assets\Scripts\Test.txt");


        for (int i = 0; i < height; ++i)
        {
            for (int j = 0; j < width; ++j)
            {
                streamWriter.Write(generatedMap[i,j] + " ");
            }
            streamWriter.WriteLine();
        }

        streamWriter.Close();
    }


    //------------------------------------------------------------------------------------------------------------------------------------------------------------------
    // Use this for initialization
    void Start () {
        //test code
        eMapStyle mapStyle = eMapStyle.Forest;
        Debug.Log("Generating Map...");
        Debug.Log(System.Convert.ToInt32("1111", 2));
        
        GenerateMap(mapStyle, System.Convert.ToInt32("1111", 2));
        
        
        Debug.Log("Map Generated");
        Debug.Log("Storing Map...");
        StoreMap();
        Debug.Log("Map Stored");
    }
	
	// Update is called once per frame
	void Update () {
		
	}

    
}
