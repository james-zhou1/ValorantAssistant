import requests
import os
import json
import time
import tempfile

#DEFAULT VARIABLES 
#do not change unless you know what you are doing
#if you do please make clear what you change and why

api_key = 'HDEV-0465ed95-8059-4c6d-b08f-40831d5c957d'# do not touch
mode = "competitive" #no caps

allMaps = {"/Game/Maps/Ascent/Ascent": "Ascent", 
"/Game/Maps/Bonsai/Bonsai": "Split",
"/Game/Maps/Canyon/Canyon": "Fracture",
"/Game/Maps/Duality/Duality": "Bind",
"/Game/Maps/Foxtrot/Foxtrot": "Breeze",
"/Game/Maps/Jam/Jam": "Lotus",
"/Game/Maps/Juliett/Juliett": "Sunset",
"/Game/Maps/Pitt/Pitt": "Pearl",
"/Game/Maps/Port/Port": "Icebox",
"/Game/Maps/Triad/Triad": "Haven",
"/Game/Maps/Infinity/Infinity": "Abyss",
"/Game/Maps/HURM/HURM_Alley/HURM_Alley": "District",
"/Game/Maps/HURM/HURM_Bowl/HURM_Bowl": "Kasbah",
"/Game/Maps/HURM/HURM_Helix/HURM_Helix": "Drift",
"/Game/Maps/HURM/HURM_Yard/HURM_Yard": "Piazza",
"/Game/Maps/Poveglia/Range": "The Range"
}

allGuns = {
    "": "No Weapon",
    "63E6C2B6-4A8E-869C-3D4C-E38355226584": "Odin",
    "55D8A0F4-4274-CA67-FE2C-06AB45EFDF58": "Ares",
    "9C82E19D-4575-0200-1A81-3EACF00CF872": "Vandal",
    "AE3DE142-4D85-2547-DD26-4E90BED35CF7": "Bulldog",
    "EE8E8D15-496B-07AC-E5F6-8FAE5D4C7B1A": "Phantom",
    "EC845BF4-4F79-DDDA-A3DA-0DB3774B2794": "Judge",
    "910BE174-449B-C412-AB22-D0873436B21B": "Bucky",
    "44D4E95C-4157-0037-81B2-17841BF2E8E3": "Frenzy",
    "29A0CFAB-485B-F5D5-779A-B59F85E204A8": "Classic",
    "1BAA85B4-4C70-1284-64BB-6481DFC3BB4E": "Ghost",
    "E336C6B8-418D-9340-D77F-7A9E4CFE0702": "Sheriff",
    "42DA8CCC-40D5-AFFC-BEEC-15AA47B42EDA": "Shorty",
    "A03B24D3-4319-996D-0F8C-94BBFBA1DFC7": "Operator",
    "4ADE7FAA-4CF1-8376-95EF-39884480959B": "Guardian",
    "5F0AAF7A-4289-3998-D5FF-EB9A5CF7EF5C": "Outlaw",
    "C4883E50-4494-202C-3EC3-6B8A9284F00B": "Marshal",
    "462080D1-4035-2937-7C09-27AA2A5C27A7": "Spectre",
    "F7E1B454-4AD4-1063-EC0A-159E56B58941": "Stinger",
    "2F59173C-4BED-B6C3-2191-DEA9B58BE9C7": "Melee"
}

allArmor = {
    #ArmorID conversions
    "": "No Shield",
    "822BCAB2-40A2-324E-C137-E09195AD7692": "Heavy Shields",
    "4DEC83D5-4902-9AB3-BED6-A7A390761157": "Light Shields"
}

allAgents = {
    "e370fa57-4757-3604-3648-499e1f642d3f": "Gekko",
    "dade69b4-4f5a-8528-247b-219e5a1facd6": "Fade",
    "5f8d3a7f-467b-97f3-062c-13acf203c006": "Breach",
    "cc8b64c8-4b25-4ff9-6e7f-37b4da43d235": "Deadlock",
    "f94c3b30-42be-e959-889c-5aa313dba261": "Raze",
    "22697a3d-45bf-8dd7-4fec-84a9e28c69d7": "Chamber",
    "601dbbe7-43ce-be57-2a40-4abd24953621": "KAY/O",
    "6f2a04ca-43e0-be17-7f36-b3908627744d": "Skye",
    "117ed9e3-49f3-6512-3ccf-0cada7e3823b": "Cypher",
    "320b2a48-4d9b-a075-30f1-1f93a9b638fa": "Sova",
    "1e58de9c-4950-5125-93e9-a0aee9f98746": "Killjoy",
    "95b78ed7-4637-86d9-7e41-71ba8c293152": "Harbor",
    "707eab51-4836-f488-046a-cda6bf494859": "Viper",
    "eb93336a-449b-9c1b-0a54-a891f7921d69": "Phoenix",
    "41fb69c1-4189-7b37-f117-bcaf1e96f1bf": "Astra",
    "9f0d8ba9-4140-b941-57d3-a7ad57c6b417": "Brimstone",
    "0e38b510-41a8-5780-5e8f-568b2a4f2d6c": "Iso",
    "1dbf2edd-4729-0984-3115-daa5eed44993": "Clove",
    "bb2a4828-46eb-8cd1-e765-15848195d751": "Neon",
    "7f94d92c-4234-0a36-9646-3a87eb8b5c89": "Yoru",
    "569fdd95-4d10-43ab-ca70-79becc718b46": "Sage",
    "a3bfb853-43b2-7238-a4f1-ad90e9e46bcc": "Reyna",
    "8e253930-4c05-31dd-1b6c-968525494517": "Omen",
    "add6443a-41bd-e414-f6ad-e58d267f4e95": "Jett"
}

allSkins = {
    "89be9866-4807-6235-2a95-499cd23828df": "Altitude Odin",
    "94c085e6-48e1-c879-2552-88bf7850c5a8": "Xenohunter Odin",
    "e02d6b2c-4e2e-a5f1-6bb8-38ac74485d7e": "Tactiplay Odin",
    "abef8114-4495-6da7-2ade-02bd0f014fd3": "Rune Stone Odin",
    "ba2592f7-45c8-8d25-1442-83971f3d95dd": "Comet Odin",
    "97af88e4-4176-9fa3-4a26-57919443dab7": "Glitchpop Odin",
    "2715f184-46cc-bec1-dd7c-e7b4d1aeb625": "Nitro Odin",
    "85c76090-4de5-3a3a-a763-f4a7b779e8ed": "Topotek Odin",
    "cda41b87-4d3a-c17c-5f6d-8990cc9c5efb": ".EXE Odin",
    "bd647d56-4542-19cd-e1ed-4fb429c78cf9": "Neo Frontier Odin",
    "157bcebe-484d-82e2-2a60-c8b4b11197ea": "Prime//2.0 Odin",
    "72e724e9-4ba4-2d12-ce1a-8db1a528b9d3": "Prism III Odin",
    "9e648b20-4ed5-1f34-87a9-979cbe9a958a": "Smite Odin",
    "5c13101a-45e4-d568-aade-d6b0dadedcd1": "Coalition: Cobra Odin",
    "57523cf0-4574-968b-9f17-168e3bdb6d0d": "Lightwave Odin",
    "65baa0cd-42ec-f99d-54a0-338d795b5824": "Sensation Odin",
    "9c134f41-4c29-1bd8-682e-178e7f349c9b": "Random Favorite Skin",
    "3bb7e1cd-4774-3b84-ab13-3fa8ca182f20": "Orion Odin",
    "67fb338a-4b21-ed70-7c2a-46bef4742b4f": "Sentinels of Light Odin",
    "02cce94a-4dc2-d11a-33cf-d8aba4e36202": "Schema Odin",
    "468fdc95-443f-f1c2-bd22-fc8e1af0de39": "Lycan's Bane Odin",
    "8dda01a6-4237-f430-ac70-c3ba677963e9": "Reaver Odin",
    "a7995818-409f-c79b-20b7-28ad642f3135": "Sovereign Odin",
    "f454efd1-49cb-372f-7096-d394df615308": "Standard Odin",
    "fa1c05fd-49fc-ad93-17d8-f0aaf11874cd": "Evori Dreamwings Odin",
    "14796249-4f23-9d52-4ea1-d8878099c01e": "Freehand Odin",
    "befa2f32-410f-a418-d8d3-b194dcf2ec6d": "Aerosol Odin",
    "14f9d94a-4add-10a9-588d-48a7111da96f": "Fortune's Hand Odin",
    "85ed3f9d-4e59-a709-8faf-bc86effb3a07": "BlastX Odin",
    "e9fce399-4abc-bb3c-8992-f887918ce327": "VALORANT GO! Vol. 2 Ares",
    "8b9855f2-4cc6-0c44-3e7c-d0b2a32c6950": "Aristocrat Ares",
    "1e5ee5bf-43d5-28ee-b2f7-96a53b783dc2": "Gaia's Vengeance Ares",
    "bb004222-4ecd-e109-e875-069c820548fa": "Endeavour Ares",
    "a609cb96-44aa-f949-c357-e4883fe664d1": "Bumble Brigade Ares",
    "ac65b631-4bd1-b0fa-3313-0da74d4eba9d": "Nebula Ares",
    "35beb433-425e-7072-7ac3-9ca95d1d1fd9": "Doodle Buds Ares",
    "e901bdeb-405f-d06c-0733-6783274d85b0": "Singularity Ares",
    "4e04647a-4cfc-64f8-4643-f6b7dbcb2943": "Rush Ares",
    "556646c0-46dd-6986-00df-a78d1c17f268": "Hivemind Ares",
    "04b1358c-4702-dd82-a135-368384b685dd": "Spitfire Ares",
    "b4803277-468a-f798-7120-718963b94d7a": "Digihex Ares",
    "e089be41-4242-b28d-1894-bbba193957a2": "Infantry Ares",
    "9d2b497b-434d-07fc-ea0f-ee96de4bffa1": "Goldwing Ares",
    "4308fe43-44c1-9fe8-d5f9-95be2bc70d51": "Outpost Ares",
    "841c9aab-4005-f7fd-3b67-24b335100fb4": "Prism Ares",
    "2edbde3f-4ccc-9251-d92f-21bc9046b999": "Aquatica Ares",
    "ff0a538f-4ee6-a3e7-f7a8-a0b5a76e027b": "Monstrocity Ares",
    "7aa16eb6-45ef-1446-fdaa-5f8fbbd04bee": "Nunca Olvidados Ares",
    "d21e2975-4586-635c-3fe4-e6be738243b3": "Celestial Ares",
    "0fac1dcf-48d0-c6c4-675e-2a8013bc879c": "Magepunk Ares",
    "cd8eb70d-443c-d9fd-48cd-98bace9d5132": "Minima Ares",
    "26bb8b5c-4b3f-e0f6-39f7-bfa6eae59c00": "Valiant Hero Ares",
    "0f4b0478-4759-911d-c44b-2a907534789d": "Ion Ares",
    "759bca71-4764-19f8-8890-239eedb78fa3": "Oni Ares",
    "4e459b3b-4dab-934f-1d77-bdbe75b6fcca": "9 Lives Ares",
    "ff555802-4633-0c8b-93f8-b8887666e3ad": "POLYfrog Ares",
    "398ef7c2-4055-980e-a8b4-669ca8bc5084": "Divine Swine Ares",
    "e4b7f196-4f05-825f-e795-a59fc829195d": "Jigsaw Ares",
    "165116bf-497a-3ffa-38dc-c58d4475e225": "Premiere Collision Ares",
    "acccab4a-4093-8a4a-f1d3-299071d763d3": "Random Favorite Skin",
    "9f3e2ba6-428f-c635-67e0-b8b7d9e3c2fc": "Sentinels of Light Ares",
    "2666f98d-4f88-8cb9-4927-629d75a6a7ad": "Sakura Ares",
    "bef693e7-419c-af25-c26c-558b3e3bb473": "Silhouette Ares",
    "43538e40-48bf-0262-d4a7-bbba3c56df77": "Snowfall Ares",
    "d29d764d-41ce-5a4d-0a96-7b8b91da16fd": "Titanmail Ares",
    "5305d9c4-4f46-fbf4-9e9a-dea772c263b5": "Standard Ares",
    "d980c0c8-492b-b8df-2d91-af99a7707170": "Immortalized Vandal",
    "e5490f71-455b-74ad-f762-f5a876d4dff9": "RGX 11z Pro Vandal",
    "c97cd8a3-44ef-8425-5bf6-11bf72128606": "Altitude Vandal",
    "ba6f2526-4ed2-8e62-49aa-ebbb04290682": "VALORANT GO! Vol. 2 Vandal",
    "4c926aa9-4f26-bc80-c486-9b888333373f": "Araxys Vandal",
    "db91451c-4309-2c8c-eded-bf842d844e52": "Neptune Vandal",
    "6191bb0b-456f-1a3e-df13-cdb0c1b8b1e4": "Aristocrat Vandal",
    "000ad7b1-44b0-9345-ea47-9cbd7dcdbb38": "Gaia's Vengeance Vandal",
    "6dee8259-4620-920a-cef7-14944bbed130": "MK.VII Liberty Vandal",
    "d3733bfe-48d7-b119-3195-249d3b46b528": "Endeavour Vandal",
    "9bf19b77-4b33-7203-9f2c-16932970622f": "Champions 2021 Vandal",
    "b0f65660-4c51-13b7-9d01-e29a1e2879b0": "Champions 2023 Vandal",
    "6c4315b8-4ff1-baaa-5aac-5790c7443353": "Origin Vandal",
    "e271a430-4282-847b-3a51-5d97839ce221": "Comet Vandal",
    "ffb65a92-4654-a7f8-1908-bf9bb18995a3": "Starlit Odyssey Vandal",
    "74789f33-4632-8052-96d7-258538721a32": "Glitchpop Vandal",
    "8e762a1f-4102-b7ce-d6a0-9690c5bfe160": "ChronoVoid Vandal",
    "522a264e-4ca7-adb0-6cf1-28b2ef938727": "Prelude to Chaos Vandal",
    "18609205-4edb-5966-cff8-0fba0230ba1e": "Elderflame Vandal",
    "917ca6e8-403e-3691-78d9-a8aa6118385f": "Imperium Vandal",
    "5b6b1eee-4185-8f83-9374-3391d0f0f742": "Sarmad Vandal",
    "9b62faf1-416c-b736-0edb-39b890f1f18d": "Nitro Vandal",
    "f7f63b78-4b12-b21e-a0e7-6bafbad81509": "Hivemind Vandal",
    "5a658084-453f-e971-5def-2bb9cf6e5e90": "Venturi Vandal",
    "437307c6-424c-6a48-9738-949b91166353": "Forsaken Vandal",
    "25980352-4407-60ff-eb27-058c1ea696cc": "Team Ace Vandal",
    "948d31a0-4c2a-9c82-2b89-fe9f2ec65036": "Ruin Vandal",
    "6f3a2a08-4f32-dbdc-8dca-628a5c840052": ".EXE Vandal",
    "23d61dbb-457a-5590-2e91-38a67a52c332": ".SYS Vandal",
    "a70fd508-44ea-8de3-3b30-d3a7eb9db42e": "Primordium Vandal",
    "9d71edb0-453c-defa-507d-57aa2935b379": "Horizon Vandal",
    "b9ee2457-481c-6776-3f5b-0ca8e8f90c89": "Prime Vandal",
    "b6f79657-4a6d-e2ae-3d64-4fbcde2958a4": "XER\u00d8FANG Vandal ",
    "41b55c92-4aeb-9c86-854a-4abcd48ea0ba": "Avalanche Vandal",
    "231528b8-44aa-1063-553e-ce8ef9846383": "Bubble Pop Vandal",
    "580dc7c6-4342-86fe-1fe8-c4b63e212fc9": "Guardrail Vandal",
    "a810ec6b-46e7-767d-7186-2cbe49e7fe1b": "Black.Market Vandal",
    "a383091d-4c7a-eb6d-0f45-e78232ede644": "Prism II Vandal",
    "11a93854-44f0-bd66-f434-3f81744ddd8d": "K/TAC Vandal",
    "1df79598-42a0-a433-0aa5-c79047c32779": "Aemondir Vandal",
    "b3a65992-469c-bab8-736e-49bbda91c650": "Monstrocity Vandal",
    "6460e252-48ef-8312-6f4f-2cb5f1b56972": "Nunca Olvidados Vandal",
    "30fd16af-4560-b2e2-7780-ee8148a0946a": "Luxe Vandal",
    "148d7f02-4259-9c17-a1a4-6fa220a56551": "Magepunk Vandal",
    "c2c7746c-496a-6372-bd7a-3186276db2d1": "Valiant Hero Vandal",
    "bbd3a52f-411e-3475-a6aa-ea88b54de53c": "Overdrive Vandal",
    "d758abc0-4d99-62d3-b22b-0db0e57de881": "Silvanus Vandal",
    "8b688de6-42d3-9430-8f38-32b0b3d1c2c6": "Crimsonbeast Vandal",
    "d8d5d7a1-4d81-8560-54bc-0692ab40f69b": "Kuronami Vandal",
    "596ce51d-40e3-dc21-b02d-b08d070a7883": "Ion Vandal",
    "7156c2ee-41fc-f8f4-d457-ebb287965c08": "Oni Vandal",
    "f328add7-4710-ab8d-95bb-409bc8278a35": "Cryostasis Vandal",
    "04d8cc84-468a-b696-85ae-a193077838ed": "Luna Vandal",
    "72c1e90b-40ca-4304-02eb-28bb2aea4ed2": "Sensation Vandal",
    "9c808029-48f5-ce89-21c5-88bf4228d2ed": "Random Favorite Skin",
    "5e080cdf-408c-a193-1eb9-7fa3af301f00": "Orion Vandal",
    "e8df3725-40de-b8ec-77bd-62a989685a85": "Sentinels of Light Vandal",
    "f946ef5c-46ab-e146-a712-1d99a1651356": "Sakura Vandal",
    "9a6c6db7-4f56-12d6-8339-6386f12090e8": "Schema Vandal",
    "6b58163f-4426-8abf-8f55-f79e3a2045df": "Lycan's Bane Vandal",
    "b788270a-420f-b824-2cdb-4d90dc7e9b22": "Transition Vandal",
    "30388628-42f0-606c-82c0-73ad43de997f": "Reaver Vandal",
    "f2b034e0-4b54-5abc-25c8-d293b6f1d247": "Tethered Realms Vandal",
    "1eb7639f-4e90-5b5b-9f53-a792103d6f29": "Cavalier Vandal",
    "e8dc658b-4c7c-2338-facd-7d8d2813560a": "Titanmail Vandal",
    "27f21d97-4c4b-bd1c-1f08-31830ab0be84": "Standard Vandal",
    "4f5ee03a-4204-5526-6941-bca4f911a768": "Evori Dreamwings Vandal",
    "44a98286-4e42-6976-937f-c982c5a31a79": "NO LIMITS Vandal",
    "e524db84-4470-2df6-b34a-778a83ac26e0": "Sandswept Vandal",
    "f2871246-441c-5f41-3dac-13947139adec": "Depths Vandal",
    "8c22a4b2-4da0-f2f2-9bd1-c89d106cd646": "Ego Vandal",
    "d9131930-4172-ec7b-f3ef-a4a33f6e0193": "Holomoku Vandal",
    "32b87592-45ad-c5a6-44ae-a9b844137c58": "Wasteland Vandal",
    "16716d68-4d36-320f-aafd-f6a6bfa5abe2": "Winterwunderland Vandal",
    "26d0c312-46c2-1912-302a-b7b8f62640ca": "Araxys Bulldog",
    "e8bf5459-4789-f9bd-bfd1-c5bcafec96a6": "Radiant Entertainment System Bulldog",
    "c610dbc8-4a90-3c86-7f9e-bfa910f75bb9": "Aristocrat Bulldog",
    "3f8be578-4e47-8afd-1e6c-cb9bb326e8b5": "Endeavour Bulldog",
    "fbe04552-445f-f202-923e-6fbd61b7e2aa": "Spectrum Bulldog",
    "f77bd50d-422e-963c-1fd3-119f80c57a74": "Bumble Brigade Bulldog",
    "aaafdaa2-429d-110c-3dd7-d4b975f1cdc8": "Tactiplay Bulldog",
    "9c056543-44af-0d36-d0f7-1196d93d264e": "Striker Bulldog",
    "8594c025-4c96-e258-13da-53a2f747bca2": "Rune Stone Bulldog",
    "4be8d0e7-48e0-eaa3-1db4-85a14094f369": "Undercity Bulldog",
    "285c6731-4451-b930-7a3d-c5a736d00f5e": "Glitchpop Bulldog",
    "8a50f044-4b00-0baa-c088-9eb666b4699d": "Emberclad Bulldog",
    "23399beb-4828-0d03-ae24-aaa62b08f796": "Rush Bulldog",
    "e7a07081-4e80-7195-9df5-6d9ddbe597f9": "Chromedek Bulldog",
    "706dcacc-432b-47e5-3cf7-2db432a8afe6": "Velocity Bulldog",
    "cc8ad3b2-4b0f-6e8d-eae0-c98cc55d002f": "Shimmer Bulldog",
    "0f2da2b0-41cc-2162-cb46-adad9ae4fdd1": "Digihex Bulldog",
    "e931dcc8-48d4-f895-48b1-199ec573625b": "Horizon Bulldog",
    "1cbbdd73-4b22-4faa-acd0-0a9d6ea1963f": "Black.Market Bulldog",
    "0f992024-4c40-2ead-311a-79bc37e5e61b": "Bound Bulldog",
    "0101d1a9-42c7-0e85-806b-d2966d9fabc6": "Retrowave Bulldog",
    "f476843a-4fc1-32a1-5e32-c18b84003460": "K/TAC Bulldog",
    "199b8536-488a-09e6-8592-ff9cf21b4ceb": "Couture Bulldog",
    "a12db8be-4f3f-b7b6-5f70-92add35b956e": "Aemondir Bulldog",
    "9c91e507-4241-33d1-c63a-aeb9ec3d9d03": "Nunca Olvidados Bulldog",
    "90e750e8-4a42-f5fc-9160-3ea5e5522c6e": "Genesis Bulldog",
    "22d2b265-4ed1-f66e-1462-44bfcc10b49e": "Libretto Bulldog",
    "325d2274-487b-8672-84d6-6db8e9798447": "Oni Bulldog",
    "d832f94c-4490-176e-c625-c3a1130cea19": "Cryostasis Bulldog",
    "c2f87e28-4c3b-5dc3-0109-ffa3a0e43f4c": "Hue Shift Bulldog",
    "dbf7b813-4931-3b45-db2b-ea8d418b2b1d": "POLYfox Bulldog",
    "1daefbff-4581-aef3-5ed6-da894d7e4cc7": "Protocol 781-A Bulldog",
    "fbf8ca06-41c9-6293-24cc-b6b292db5cf7": "Premiere Collision Bulldog",
    "7baa9f5a-4ac3-804a-2e47-4da916de0b79": "Random Favorite Skin",
    "b778fd63-4e21-b400-db3b-d1807e3f4edb": "Transition Bulldog",
    "decd0962-453a-1551-47e1-1287aafb5a27": "Infinity Bulldog",
    "724a7f42-4315-eccf-0e76-77bdd3ec2e09": "Standard Bulldog",
    "006d6b0a-47ba-a909-ade5-0cba66dd5829": "Tilde Bulldog",
    "0c0cbd13-4601-e6c1-0180-2181e2461c36": "Gridcrash Bulldog",
    "8c7238c8-4161-a5ac-69f2-129f8a4ce5fa": "NO LIMITS Bulldog",
    "f580899d-49c4-8bf8-9718-c9a6a38dd503": "Convex Bulldog",
    "4e6341f9-4851-603d-daff-9185f007d3dc": "Depths Bulldog",
    "e9164092-4c79-b6ae-b844-ba97f566958d": "Holomoku Bulldog",
    "9bba8d9a-461e-9783-fcb7-f1a92192fb3a": "Varnish Bulldog",
    "3d71065e-4f0b-19a8-26d5-129cddeb013b": "Task Force 809 Phantom",
    "499acf05-4f79-e345-3714-57bf7aa163ea": "RGX 11z Pro Phantom",
    "fac0cea1-45a9-1549-c120-af8f0150e562": "Xenohunter Phantom",
    "0acbabbe-4f4c-f643-284b-f69029abb54e": "VALORANT GO! Vol. 1 Phantom",
    "4eb45d71-4fa4-be4f-7409-cf92123f1d22": "Radiant Entertainment System Phantom",
    "7ae63121-4cf0-b4db-00ed-eb8ef05572b1": "Gaia's Vengeance Phantom",
    "980fa063-436e-e51f-c38d-70a5b93a0f1c": "Spectrum Phantom",
    "d556b1c2-46fa-fca4-0516-5c887fd2352a": "Piedra del Sol Phantom",
    "052a0ba8-48a5-acd4-f989-87b067140b35": "Composite Phantom",
    "8c72ae0b-4357-1a75-ad62-fbaec7b64f92": "Champions 2022 Phantom",
    "4bdf9f7c-4957-ff27-6e2c-f4acbbcf1ce5": "Tactiplay Phantom",
    "2371d9e1-498c-1ad1-4f10-d1a339c7fda2": "Radiant Crisis 001 Phantom",
    "57f91d68-4cda-76c0-c258-7ba507cd6f87": "Nebula Phantom",
    "ed3ac995-4fd1-3079-27aa-4aab84447833": "Undercity Phantom",
    "25a7f0f2-4bce-7e45-b4b0-ca9264f5dfcc": "Glitchpop Phantom",
    "2aac8bb3-4cfa-b806-21e4-5a8e9904caa4": "ChronoVoid Phantom",
    "43da7fa1-4b01-7e91-d68c-85b0f63c0d8f": "Emberclad Phantom",
    "2d1472fd-458c-515a-c4e4-ceaa50c84187": "Abyssal Phantom",
    "3a091315-4e87-31d5-7cdb-27804a177fd2": "Doodle Buds Phantom",
    "5eec4ce6-443d-e9b5-4c5b-2b967d426bd3": "Singularity Phantom",
    "cd07ba8f-4dae-0410-582e-71acdef102ce": "Sarmad Phantom",
    "8db507b5-4d57-96e0-000e-2d8c8af79550": "Rush Phantom",
    "4b73b610-4096-60c1-1969-f2b05b53fa43": "Chromedek Phantom",
    "a17d4eeb-46e5-a041-ae7b-a2841ac6b36e": "Velocity Phantom",
    "f7a779db-4835-6561-ce1a-d1921a24de46": "Team Ace Phantom",
    "d34edafc-4e48-b2d7-6163-08bf054d3d80": "Topotek Phantom",
    "52417dc8-48b7-111a-b63b-5db108b2e63a": "Neo Frontier Phantom",
    "98c9bc4e-4fb3-206f-3f6b-06a17b53e95b": "Soulstrife Phantom",
    "34560475-4eaa-d2be-b37f-908463413482": "Primordium Phantom",
    "44b7b110-46bf-ccbb-2613-29a5df296461": "Prime//2.0 Phantom",
    "c38dced0-454d-d296-522e-6f8643decd3b": "Avalanche Phantom",
    "2f1da068-4779-d711-85ae-90840f0e38fa": "Bound Phantom",
    "6586a7db-4041-6a29-f37c-d6817657caa5": "Prism Phantom",
    "a903e567-480f-a3f9-adb8-1da714a2d63c": "Serenity Phantom",
    "5b43d27b-419c-f2bc-53fe-d7829dad46b3": "Ruination Phantom",
    "e13afe1e-4734-2094-fee8-9db016e4d54a": "Kingdom Phantom",
    "8f82cff0-44b9-b792-8dd2-b2be8538421b": "Kohaku & Matsuba Phantom",
    "8d3ead4a-4421-f1f2-4292-ecac859fc135": "Smite Phantom",
    "228192a7-4d45-0a11-1439-b8b110141a43": "Daydreams Phantom",
    "b294ba9c-4e05-ebb4-b2be-4e8799ee3fc7": "RDVR Phantom",
    "8c0cc1e8-4c1b-20a0-122d-16b4334d1b80": "Celestial Phantom",
    "f2531d6f-40d8-ad18-4e74-ed812e0a6b1f": "Magepunk Phantom",
    "13f553a1-4124-7c29-05e9-e7932fdeabb6": "Spline Phantom",
    "2e3538f1-450f-cfe6-f93e-73862cd39314": "Minima Phantom",
    "41892314-4a99-0048-1838-e38cd680ea26": "Galleria Phantom",
    "25824735-478d-30b7-8fc9-95b1999f9d3b": "Silvanus Phantom",
    "e86bf7e4-4dd3-fbee-533b-fa875344bbaf": "Ion Phantom",
    "36791b03-452d-8dad-0091-898cc28d2196": "Oni Phantom",
    "4cd5b984-4ef3-017d-36f1-5d8129a95fec": "Switchback Phantom",
    "762aca85-4bf4-73a5-932a-2aa8407c31b3": "9 Lives Phantom",
    "3a204da4-4aa4-d02f-73a0-55867bc8d501": "Hue Shift Phantom",
    "56f075b7-4171-a977-90ac-d5ad786f1478": "Aero Phantom",
    "909daea4-49ab-7b99-46fb-aa8c9e6fd837": "Artisan Phantom",
    "9877d50b-43b1-837a-802a-bf8a3b98e2dd": "Protocol 781-A Phantom",
    "29665396-4dc8-c409-5e38-228949690f1e": "Lightwave Phantom",
    "fff73ad4-4d46-a6d9-43f1-51b633845434": "Random Favorite Skin",
    "8588c8ff-47a5-3900-0518-d6a80b31ba35": "Orion Phantom",
    "a8652d02-458c-461c-8aa8-b7a520455023": "Sentinels of Light Phantom",
    "80b755a5-4fce-0529-8678-969eab271efe": "Shellspire Phantom",
    "a74f77fd-4e69-f16e-b1eb-ceb5198f423d": "Snowfall Phantom",
    "044b28ba-4c3b-d315-140d-d9a249da5567": "Reaver Phantom",
    "42fe7bf8-40ba-b1f4-df5e-34a6f51f29bf": "Sovereign Phantom",
    "d67b929f-4431-61c0-286e-3ebf3d11c4af": "Recon Phantom",
    "ce85f078-474a-eae4-3844-03a49625df15": "Mystbloom Phantom",
    "1f835677-4ed7-fec2-6b80-c3ac384323f6": "Infinity Phantom",
    "fb86d3b7-45f2-6a97-c468-51ab29cb4a04": "Reverie Phantom",
    "337cb216-4a6e-d85d-88c2-f29ab317784c": "Standard Phantom",
    "034de367-470f-28e3-26e3-dfaa8e598acc": "Fortune's Hand Phantom",
    "e0cf9566-452c-1501-43b1-778e69c60dbf": "Tigris Phantom",
    "59af9c5d-43ee-1360-f3a7-a9a6ff6e478b": "BlastX Phantom",
    "a5c64455-4fd0-9207-fc97-e086af99a2a6": "Winterwunderland Phantom",
    "d1b142ce-4a6a-cdcd-7f64-eb970cacfc16": "Convergence Phantom",
    "6c9206df-444d-8c81-789f-02af9b99ad61": "MK.VII Liberty Judge",
    "d7717613-4ef6-b314-6a95-9e8a1ee603bf": "Piedra del Sol Judge",
    "70d69cbe-4380-9b25-2a21-46ad9817318e": "Bumble Brigade Judge",
    "e413125e-40c6-cccd-de35-f28e34c57442": "Undercity Judge",
    "28a659a4-439e-fcd0-6236-d39979ee5c51": "Glitchpop Judge",
    "4d2ec3f4-446e-a501-74d8-5ab750f50984": "ChronoVoid Judge",
    "0221b120-444b-6d1b-fc50-e4a98e470eb2": "Elderflame Judge",
    "e661e655-421f-0f19-3092-c8a668036ac4": "Imperium Judge",
    "f6db3976-4c70-c3bf-01f8-dca6d335319a": "Rush Judge",
    "fdf7fef7-43db-9409-be4c-44bc0b5084f6": "Team Ace Judge",
    "ce38c32d-43e6-e840-3981-668454383e22": "Shimmer Judge",
    "fbd23fdf-4d7b-8a50-afa5-c3ad6e7266e5": ".EXE Judge",
    "4fd7995b-492c-7cfd-36f8-a68ddf07f3e5": "Digihex Judge",
    "37735cf0-4c4f-6efd-6222-8582622d68a0": "Goldwing Judge",
    "3d8f9c7d-4259-4710-1f94-0fbc4f25035c": "Hydrodip Judge",
    "caf6ad17-4888-3241-230d-849c48d21473": "Bubble Pop Judge",
    "400d71b1-4090-6abf-224e-21938569fe24": "Outpost Judge",
    "1c7e4522-49f7-4125-a7ca-1f8c943c804e": "Bound Judge",
    "1fc3f066-4211-d65a-42ab-b287c6bb2448": "Prism III Judge",
    "3a1c857a-4671-0667-8efe-ee90b8ba1e5a": "Serenity Judge",
    "da3cedea-4f2e-c501-ec79-438433ffabdf": "Kohaku & Matsuba Judge",
    "5324bc65-44aa-1a16-ede4-0e9b56f35d0e": "Smite Judge",
    "fab8bdfa-49c1-dfe1-5a15-538dc3f288af": "Daydreams Judge",
    "0cba5a5f-41ab-ed7d-158e-4fb92ab25c47": "Iridian Thorn Judge",
    "57ad1e5d-4289-4de0-7926-899cef10db37": "Celestial Judge",
    "5237cfca-4d83-6190-a7f9-d2bdc117ea67": "Luxe Judge",
    "0b8816a2-42ad-9353-c591-f7863981d7fe": "Coalition: Cobra Judge",
    "5e342c5c-4757-4c4e-ca7c-a4b97930308b": "Crimsonbeast Judge",
    "5d217dd0-4f2c-cfca-274e-3f8f9d518b13": "POLYfox Judge",
    "a913d712-4c29-d7f4-0f8a-d790e023ba3c": "Divine Swine Judge",
    "ba93a991-407f-0c47-2d26-72a4196b4164": "Jigsaw Judge",
    "8e27a0b3-4dc9-e2a7-e33a-29a616efc244": "Sensation Judge",
    "68f2e92e-4c94-8104-ed99-03925bbc71e8": "Random Favorite Skin",
    "00947f74-4daa-dd59-32cb-4fa1ac6611af": "Silhouette Judge",
    "a07941d7-42dc-5083-97a1-af850ca6fa26": "Snowfall Judge",
    "bd034009-469c-88a6-41aa-278dd54b12e6": "Sovereign Judge",
    "5c8d1196-48d8-2bbc-fac0-57af71a18c97": "Mystbloom Judge",
    "acd26127-48ff-8b9e-7ba6-b989af8a4b24": "Standard Judge",
    "91cea710-495b-fd95-9e7a-6c928a0c5449": "Tilde Judge",
    "4b77be03-4410-1ac5-0b9e-82b326cd990f": "Gridcrash Judge",
    "03751fa0-46db-0df3-b8cb-99adf373ecda": "Convex Judge",
    "87591a69-47c1-a052-ba85-33a8097a0b07": "Varnish Judge",
    "613152c2-47cf-be72-9b45-b6958117b220": "Altitude Bucky",
    "0666931c-4580-efd0-af47-afb9f2f72e55": "Xenohunter Bucky",
    "892b5053-4c0b-149e-38d0-c3a8d6f24384": "Gaia's Vengeance Bucky",
    "001e4ce2-4b30-8203-365a-828e2e3a5826": "Piedra del Sol Bucky",
    "96495eb3-40db-cb5b-1c69-17a3dde58ee3": "Origin Bucky",
    "31072cda-4041-b4f0-119a-3692ea598321": "Radiant Crisis 001 Bucky",
    "1322a9a8-49ad-bc3a-2319-fb866e21334c": "Red Alert Bucky",
    "aa6162a5-4c73-1c6f-5c69-9b9082e321fd": "Surge Bucky",
    "4a1d582d-4c3b-6595-57b6-e3b2cf0ee543": "Topotek Bucky",
    "82204cf0-4a3d-2802-6eb9-9eac53472a3f": ".SYS Bucky",
    "d493bec2-4e3f-19cd-8363-b1921489413c": "Horizon Bucky",
    "8f26c1e0-46b7-72d2-8307-11b03f3332f2": "Monarch Bucky",
    "50b0db3d-46a9-5c2f-2e57-7fbeedf30362": "Hydrodip Bucky",
    "89eebdb1-4df6-0a1d-8988-f495cca4badb": "Prime//2.0 Bucky",
    "a6b07d50-4731-2775-042e-a896cb51bf13": "Prism II Bucky",
    "0344b901-4500-8843-fd9c-97b63ee729cd": "Retrowave Bucky",
    "75e55415-45ce-b48b-b471-84bef2368e33": "Kingdom Bucky",
    "ce298668-4034-ebe2-3324-67963d4d3629": "Aemondir Bucky",
    "d95fe9cc-4b39-6f54-1912-d796b5912481": "Iridian Thorn Bucky",
    "5ac14aef-41cc-a0c8-895f-e1a69b33aeff": "Magepunk Bucky",
    "4fca7cd4-48b6-130f-01fc-fa87974bb622": "Overdrive Bucky",
    "2a0700dc-4181-ae19-2b49-818b24dceacb": "Galleria Bucky",
    "daf3c0d8-4c6f-23c0-20cc-96b0386b548f": "Genesis Bucky",
    "31f6f214-4379-749a-9285-04a5561e2d03": "Ion Bucky",
    "7da96a2a-43ce-91c2-28f9-0c95529d133e": "Oni Bucky",
    "1a97f146-4fcf-5a04-140e-4390feafaa73": "Artisan Bucky",
    "26582dc8-43dd-15b6-a31c-739b90302bea": "Lightwave Bucky",
    "ed407bc7-4949-3131-b84f-d6be83b63a15": "Random Favorite Skin",
    "0dc9a874-41c5-e582-9a36-37946043346c": "Gravitational Uranium Neuroblaster Bucky",
    "058322eb-44fc-8dee-947c-8b95a550ba10": "Panoramic Bucky",
    "e6eefed6-4d10-5794-4859-6d9ab5ff1d66": "Cavalier Bucky",
    "1ecb1abc-41a4-f789-39a5-4583f043d688": "Titanmail Bucky",
    "70c97fb2-4d79-d4bb-5173-a1888cd4bfd9": "Standard Bucky",
    "cf2cc18c-42ec-3fb0-4ca7-3583373a33ab": "Aerosol Bucky",
    "1bd0b030-49b3-4733-d6f0-28bcb7ed6df2": "Task Force 809 Frenzy",
    "d5ea8ae9-4055-9b65-1f39-ed97372d887a": "RGX 11z Pro Frenzy",
    "a4b0cd8b-40dc-41e3-646d-d58802b2e310": "Xenohunter Frenzy",
    "7d05d1ce-4bf2-fa96-d8f4-dca86052e3d2": "RagnaRocker Frenzy",
    "cceb25d7-41e7-1944-515f-2eb5695fd5cc": "Origin Frenzy",
    "5596d764-4b62-210b-59db-7982e9d4c23f": "Glitchpop Frenzy",
    "e208b1f1-41bc-9750-35c9-448cbdd4c200": "Emberclad Frenzy",
    "4fb9ea7d-45a6-9154-7a46-648781b081c4": "Elderflame Frenzy",
    "3fd33106-4816-c257-d27f-2b86c5d76c66": "Sarmad Frenzy",
    "a010c5fc-4343-067d-4dfb-ee836ec0a45f": "Rush Frenzy",
    "5c0965bc-4860-94a3-a133-b29b08f75051": "Venturi Frenzy",
    "5947209b-4864-fb3b-bc48-74a7924e4412": "Team Ace Frenzy",
    "d6af3716-4ab5-8204-a2f4-1eb4ffc51088": "Swooping Frenzy",
    "17162b11-45fc-5b66-2e49-79ac9d60032c": "Horizon Frenzy",
    "b543f6c4-4404-4e5e-1fcf-67a0cd8e9bc4": "Monarch Frenzy",
    "8256eb2c-4368-9da8-521f-379c3793dce1": "Hydrodip Frenzy",
    "51446541-47dd-b661-470e-9d89b3b6a33b": "Prime//2.0 Frenzy",
    "e89209cd-4ec7-53ad-2d34-a8807764a60f": "Guardrail Frenzy",
    "08bfb08f-48cc-2699-2f5c-aabec43dd43a": "Couture Frenzy",
    "068cf886-4688-6609-e79f-d4b6afe1d3cb": "Blush Frenzy",
    "a878b90b-4d32-6e85-d49e-82bfba69471f": "Nunca Olvidados Frenzy",
    "307dbbc2-442d-b92b-0af2-278a8505672a": "Celestial Frenzy",
    "0ce7539f-487a-9c4b-5a41-3fa338f5abcf": "Tacti-Series Frenzy",
    "bb46d680-4e05-bacd-6ecd-11895d2f22e7": "Coalition: Cobra Frenzy",
    "87643553-437b-d057-8f06-25b5bd723378": "Moondash Frenzy",
    "906dcda9-477a-6d09-f85d-599ccb86e168": "Ion Frenzy",
    "7a20502f-45b2-6781-b408-08bc86c5e5e2": "Oni Frenzy",
    "5bb5acb1-44dd-184b-484e-319188ef78eb": "Spitfire Frenzy",
    "12e6f520-460b-e69b-0617-bab9fff1a134": "Aero Frenzy",
    "fa0bb312-4446-a061-9b06-ee88314e07fa": "Divine Swine Frenzy",
    "f67d4d78-4567-f8ca-010b-18919c49aa05": "Lightwave Frenzy",
    "531135cc-48cb-68bf-8c99-149e46670c80": "Sensation Frenzy",
    "7b82c605-44bb-aae9-55bf-a4afef323553": "Random Favorite Skin",
    "d02d21e4-4b57-945e-c504-e8af1bdd488c": "Orion Frenzy",
    "9977a737-4bb5-8af1-ea9f-e1accc80ab1f": "Silhouette Frenzy",
    "b6d415e1-41bb-0a8c-9991-49b7d70b1faa": "Shellspire Frenzy",
    "daaeb0f9-413a-732d-e6f0-598b9dff65a7": "Sovereign Frenzy",
    "324c837d-4e55-a259-0852-92bc27e724da": "Titanmail Frenzy",
    "f7fc6f86-4599-e131-e392-d6b2dfabd8cb": "Live Wire Frenzy",
    "f06657f3-48b6-6314-7235-a9a2749df5b9": "Standard Frenzy",
    "79005812-4d5c-cc6d-e2bd-19bc86c29349": "BlastX Frenzy",
    "a1f91e04-40ff-76a0-4439-028a511e6f36": "Holomoku Frenzy",
    "29c91578-4aea-6177-2d0f-469f77ca9616": "Convergence Frenzy",
    "ea9da25c-422d-d256-a970-cbaeb55542bf": "Resolution Classic",
    "0d065a05-4ef3-44b6-95dc-76ac19038d4b": "Fiber Optic Classic",
    "111680fd-4562-f658-af1c-ed8f9cfe9f9c": "RGX 11z Pro Classic",
    "5077ebbc-4adb-bb8e-762e-6cb6cc9262f4": "Intergrade Classic",
    "b06e13ff-4f19-c750-ffcd-8084dfc3bbf5": "VALORANT GO! Vol. 2 Classic",
    "46f32f75-4fc8-7121-8a77-db8db43afc67": "Spectrum Classic",
    "34919680-4f00-554b-0c2b-95acca7d0d36": "Pistolinha Classic",
    "6f6b606f-4d9c-c071-b817-9ea59d5b02d3": "Striker Classic",
    "a95d08be-4e56-1189-801b-d9aa4efe32fa": "Radiant Crisis 001 Classic",
    "41fce834-4c76-a0f4-2cf8-cca3ae879eab": "Red Alert Classic",
    "ac14dca7-408b-7e8f-8ed0-99b8ed1ffe98": "Undercity Classic",
    "8b2598eb-4db9-6338-4a25-c780402c780e": "Glitchpop Classic",
    "3af7fef0-48cd-64d3-cead-dcb9cd07865a": "Finesse Classic",
    "6cc70eae-4297-91d5-adb9-efa48004da77": "Surge Classic",
    "10354287-40e9-4087-85c5-aea7289d31f2": "Songsteel Classic",
    "c612138e-4007-6d0c-64ad-3690c65ee4a7": "Forsaken Classic",
    "9a6d4520-48a6-d46c-5a3f-2ab0b10dd8f6": "Shimmer Classic",
    "144ac55d-42b9-338c-fb32-c9a31f4da5bb": "FIRE/arm Classic",
    "1180c78d-4b0d-491e-efdc-cfa5d948fa27": "Goldwing Classic",
    "d653f4a7-4e92-2559-0a97-2c9d46d009b3": "Prime Classic",
    "6b6a219d-490a-45f1-1e5c-40bbf3df5f28": "Avalanche Classic",
    "d90a940b-4040-4c7b-7a9b-7ab574429226": "Bubble Pop Classic",
    "a6b46cef-4ed2-79e4-d49a-459180cdbd23": "Black.Market Classic",
    "94bc4d7a-4b88-4c84-efef-969cdf84019e": "Bound Classic",
    "62abf8b2-4511-131d-42c9-81a5efd1b901": "Prism III Classic",
    "e72d72ab-4284-1469-b544-478a811a29a6": "Kingdom Classic",
    "be7cf362-4993-b9e4-9ba9-cdac6c99b8e4": "Kohaku & Matsuba Classic",
    "22fdc42d-4ad6-2bec-8033-8a8bdf178826": "Smite Classic",
    "9a890a05-4173-c5af-743c-f2b423fae42d": "Daydreams Classic",
    "750d4f04-4fea-391b-fa8b-539815a63164": "Spline Classic",
    "815c8781-4f80-9a81-19c3-5f97c93aab90": "Tacti-Series Classic",
    "2f9f4637-4377-b55f-97a1-1e8974e29b27": "Galleria Classic",
    "3d238836-4e86-67bf-8664-52bb0e8a1a83": "Switchback Classic",
    "edb386a1-4d02-4fd0-2f84-f8bf6434e5c4": "Cryostasis Classic",
    "f3f962bd-4a19-b363-e939-6a91b897a28c": "9 Lives Classic",
    "c4c0edc9-4ce3-3945-81f5-1bb80aeb22fe": "Premiere Collision Classic",
    "3e3ad47a-4383-73f1-4d92-1693059dae8f": "Random Favorite Skin",
    "81ddbfcd-4081-8341-ff76-ad8cdb26ce4c": "Gravitational Uranium Neuroblaster Classic",
    "223852c7-4898-01e7-c813-5db4f1769e3f": "Panoramic Classic",
    "6ba7a7a0-4057-4d5c-7c98-579f232db298": "Sakura Classic",
    "464887be-4a07-690e-2d02-e187c8bbe8d5": "Snowfall Classic",
    "706f4a29-4a95-7370-c983-1a8b167e38b7": "Infinity Classic",
    "8bc021a4-4832-300e-2844-afa3d1d9465f": "Reverie Classic",
    "24aee897-4cdc-b0fd-e596-1ba90fa6d1b2": "Standard Classic",
    "47d5e54a-48e5-b62a-5cf5-3cb7efc12e90": "Final Chamber Classic",
    "481b782e-44c1-a68a-b043-bb91ea1badad": "VCT x 100T Classic",
    "442b379d-4a57-9469-c393-65962a25c950": "VCT x AG Classic",
    "01af54eb-405f-029d-80e6-c681346dc0f0": "VCT x BBL Classic",
    "15104eab-4b4c-0f67-0dbc-efb67e114e7f": "VCT x BLD Classic",
    "a13dc2e3-4b2e-6551-df89-3f857c4a4612": "VCT x BLG Classic",
    "429437e4-4bc1-70b1-b3d3-358d9f8b199e": "VCT x C9 Classic",
    "17c3d20d-4955-cb76-cdce-c6a7fc0d1eb2": "VCT x DFM Classic",
    "7ef0e069-4786-1954-32d8-50ad393be96b": "VCT x DRG Classic",
    "027346aa-46a5-875c-4640-ee96ba581ccc": "VCT x DRX Classic",
    "2a485c83-4ad9-b318-9276-24a947cc93f8": "VCT x EDG Classic",
    "6b03d2ad-4c86-e541-ea28-82877cc12c7b": "VCT x EG Classic",
    "c84c61cb-4da0-1669-70b9-8297bd28db6f": "VCT x FNC Classic",
    "1fb7b866-4c0c-4128-0535-0a9b9fac3965": "VCT x FPX Classic",
    "5c1ce621-45a0-7ec9-8440-c39214d070a3": "VCT x FUR Classic",
    "3ef741a2-4822-96ae-371a-87b3908421a5": "VCT x FUT Classic",
    "f04917ec-4104-7127-dd82-00bea157662b": "VCT x G2 Classic",
    "854a1c7d-4674-d9d7-ac18-849aa4d5e708": "VCT x GEN Classic",
    "80bade28-4b3a-af0a-97ff-e3bccdeaed6f": "VCT x GE Classic",
    "17f0db96-4e2d-6bfd-da2f-aaa54a1d3ffc": "VCT x GX Classic",
    "71e4a922-4bfd-1c56-234c-e39675d362b6": "VCT x JDG Classic",
    "c6c66163-468e-b7dc-e1c3-878caaea54a4": "VCT x KC Classic",
    "bbefc94e-4864-bd6e-5cf5-b79506ee645f": "VCT x KOI Classic",
    "7b510be9-45a9-89f6-5440-fd8747345c61": "VCT x KR\u00dc Classic",
    "bd1f700a-443c-0cd9-4647-47bcda8bf42b": "VCT x LEV Classic",
    "0aa66a21-41d9-8c50-f2ef-3988b57bfd52": "VCT x LOUD Classic",
    "0c38772f-4aba-42ce-d14c-15905477fad8": "VCT x M8 Classic",
    "22c06960-430c-bc82-66e8-1b8c8b5f8640": "VCT x MIBR Classic",
    "7e0a5637-4cd4-cbea-cd3e-b4852b182424": "VCT x NAVI Classic",
    "ef59bd63-41f9-fff3-0d02-72bcbd730688": "VCT x NOVA Classic",
    "ccaeee25-4855-8ebd-3650-969c587984cb": "VCT x NRG Classic",
    "d3518639-4f2b-1eb7-f246-d7bbdeeeefb2": "VCT x PRX Classic",
    "920bee4d-4a1f-55f1-e879-c5925b6a2e06": "VCT x RRQ Classic",
    "f336402b-48e3-2edf-3c5c-c68c35daa20e": "VCT x SEN Classic",
    "eb08a6cc-4d1f-3bbc-2254-efb03acbdecf": "VCT x T1 Classic",
    "fd244905-46ad-9bb4-d921-3e8e096ab745": "VCT x TE Classic",
    "41d4f33c-47f2-0553-44d9-5cbd73e017d8": "VCT x TEC Classic",
    "11b7da6e-48b8-04e6-1cab-b0ae0f1d5ace": "VCT x TH Classic",
    "9d7fcd48-43c6-867e-ff71-7497b3cb7f43": "VCT x TL Classic",
    "53f1d218-40df-272a-b05a-c3aac215f5a7": "VCT x TLN Classic",
    "0624e073-4f0e-f0bf-0193-09a5b3513a7d": "VCT x TS Classic",
    "b7a74aa5-4716-a026-85ad-cc92837fc1ca": "VCT x TYL Classic",
    "4071c280-400b-23a6-a43e-7e8385162185": "VCT x VIT Classic",
    "2637724b-410f-55c7-4002-36ab136bae08": "VCT x WOL Classic",
    "d634b446-4ca6-59e0-2b62-4fa521c2d222": "VCT x ZETA Classic",
    "d0fbfdee-4961-cf51-24a4-4a853ee9fd0c": "Flutter Ghost",
    "86564070-4e0e-fae7-1c2c-e28f044076d6": "Fiber Optic Ghost",
    "3714831b-4b90-bb6b-4185-7fb05ba9b9a2": "VALORANT GO! Vol. 1 Ghost",
    "9ad4308f-4ffb-03a8-25c3-7a80b60579de": "Radiant Entertainment System Ghost",
    "daed0e44-4ab6-22b4-a5a5-57a4957a056b": "Gaia's Vengeance Ghost",
    "cd281dcd-4276-1def-11d9-74a4a72db204": "Endeavour Ghost",
    "9db45d13-4cc3-4b6c-4801-459b79f8cda5": "Piedra del Sol Ghost",
    "cc29eecb-4b93-2b73-2c04-e284565d9b78": "Bumble Brigade Ghost",
    "2204f110-428c-3e94-a188-0fa1b093c2be": "Comet Ghost",
    "df65f29b-465c-827a-7c34-15be149b883e": "Starlit Odyssey Ghost",
    "e223e993-45f5-013b-4259-11b263184752": "Topotek Ghost",
    "d2ed8432-44a2-fb53-cd5f-089251862942": "Spitfire Ghost",
    "67d3e2f7-4b73-7598-0027-63bd9e2e5fcc": ".EXE Ghost",
    "a1d3a9e2-4f61-b1f7-3a01-cf867264d1cb": "Hush Ghost",
    "2fcdb6c8-4183-0079-13fe-2cb51da0b87c": "Soulstrife Ghost",
    "a754999a-4acf-0fca-a155-3684f176b5fe": "Digihex Ghost",
    "65ce6a98-4867-b695-279f-819c44ec6f95": "Infantry Ghost",
    "44be88b3-4a0e-64c8-950d-66a969e71f7e": "Goldwing Ghost",
    "1c1ea3cf-4146-de0f-7e6a-828f68f0bb63": "XER\u00d8FANG Ghost",
    "377ea8ac-46bf-52da-3173-109c2950dc9d": "Outpost Ghost",
    "8163db1a-4e3c-8f11-92fd-bc9e26253593": "Prism Ghost",
    "d8314b6c-45fc-fbda-a797-569a24c11bb9": "Serenity Ghost",
    "8a513c24-4c4d-ac15-6066-a1b2ff577041": "Ruination Ghost",
    "cb98b0d6-4e26-973c-c10d-a38637d04b65": "Luxe Ghost",
    "33824a13-453b-0636-4ec4-e19708aa934e": "Magepunk Ghost",
    "48486283-48d8-cb8b-01c9-9b9409ab1d4d": "Valiant Hero Ghost",
    "e552accf-4c90-0221-02c2-889b6fe10d8f": "Libretto Ghost",
    "8dfec665-4836-d498-2896-08a16c092133": "Artisan Ghost",
    "f20bdd80-4cbf-67a8-106e-72bbf94336aa": "Jigsaw Ghost",
    "4ab1d112-4ae0-4841-11f8-b198cb847862": "Luna Ghost",
    "b4903002-4687-1953-847a-e0b09a2b2726": "Random Favorite Skin",
    "4725c2c4-45b7-d9ab-ff4f-a79c3b2dd9ec": "Eclipse Ghost",
    "1a9afd32-46fc-43c1-ab92-0a95e912805b": "Lycan's Bane Ghost",
    "c7261be6-47d2-ef86-82f4-6a844e45d33c": "Reaver Ghost",
    "efbd92f3-4abc-b077-76fd-dc805b3d72a0": "Tethered Realms Ghost",
    "a9890917-41ea-eb55-47e7-ee990a87fa4e": "Sovereign Ghost",
    "bb28991f-4ca9-ca54-962d-31b68c838625": "Recon Ghost",
    "153b2b33-4e6c-fb98-42dd-5a9819649dc7": "Cavalier Ghost",
    "1c63b43b-43c4-04e4-01c9-7aa1bffa5ac1": "Standard Ghost",
    "2a8a2ff3-44f0-6e8f-8e37-7282113177cf": "Evori Dreamwings Ghost",
    "35dfbae0-4be6-3f47-2a1d-4aa0c5599e1b": "Freehand Ghost",
    "fbba3f7e-402a-92f3-b3d6-a69d653e5204": "Gridcrash Ghost",
    "bc46c754-42a6-f3e1-ff07-5396d514b9f1": "Fortune's Hand Ghost",
    "3f59b69f-4391-b0ee-705e-329175931502": "NO LIMITS Ghost",
    "69addb00-4eb5-eebb-c4c5-2296549cba6f": "Depths Ghost",
    "b84df096-4096-e9c4-0869-8e83e7fc5476": "Ego Ghost",
    "0a6edcf0-4a64-0ed5-1b10-0e96c2eb4cb4": "Vendetta Ghost",
    "845a6945-414c-c916-6041-e4a3ef1108cd": "Winterwunderland Ghost",
    "e24330ef-4315-512c-4588-95a601995888": "Soul Silencer Ghost",
    "34f735c0-4fcd-b4fd-fb34-fbab97b42a41": "Wayfarer Sheriff",
    "c2aee89c-4f9c-47a9-8dc0-f9a53535d508": "Mythmaker Sheriff",
    "304e1a7a-411d-2d27-dad6-c09702b5ea2f": "Immortalized Sheriff",
    "1946d021-4c01-2cc7-d29e-4eb9e90279cd": "Altitude Sheriff",
    "840f12d8-467b-1a5e-f79c-b893b72b2fbc": "Aristocrat Sheriff",
    "db5db925-45cc-9a63-3351-6ba36ef1bb9c": "Composite Sheriff",
    "55ef0ffa-44fe-03ac-dcf0-1982df0857aa": "Nebula Sheriff",
    "e1fdd246-4a6c-af26-f0a0-65a48f2586da": "ChronoVoid Sheriff",
    "79a78823-41dd-a2e8-7586-12bc8154d2d9": "Abyssal Sheriff",
    "9eba83e5-4084-300e-d001-fd8152dc6522": "Imperium Sheriff",
    "bfd9e773-4376-1f6a-98f2-dc93f0c0607c": "Singularity Sheriff",
    "2674c385-4397-0383-04df-988d8d6fd2c8": "Surge Sheriff",
    "3850ea5a-4e51-d913-7a44-48b2589e06b9": ".SYS Sheriff",
    "b73f455a-4d77-44e7-fd90-1db9db82a8f6": "Neo Frontier Sheriff",
    "4f1fde01-4130-0ae7-1320-6fb2f2fb6ab9": "Protektor Sheriff",
    "3194b53a-40a9-a419-a8a6-43b1a53cd0e9": "Prism II Sheriff",
    "570e61cd-4057-85ef-2da0-e4bbba48d706": "Retrowave Sheriff",
    "95eb82e2-4859-5564-7b3b-ddbf2fb8088d": "K/TAC Sheriff",
    "db41461d-4cee-b397-09ff-f2b0d8f012f4": "Aemondir Sheriff",
    "f8dfd0ad-496b-2b31-fff8-dea9de2f04c0": "Monstrocity Sheriff",
    "6b57a839-4f3e-8df9-4b05-0db2c9fa1fae": "Iridian Thorn Sheriff",
    "6460edbf-458d-bf61-7519-519305ba5da2": "Magepunk Sheriff",
    "cb89c7bb-445e-dfec-ad4a-b0ba37271329": "Signature Sheriff",
    "46ffe3ea-4fb5-7773-6242-f5b57bf53ef8": "Minima Sheriff",
    "208bdc02-451d-60e5-196c-47ae67f150fc": "Overdrive Sheriff",
    "721ab58c-4ba2-b7ae-c571-0993d9799fc5": "Silvanus Sheriff",
    "97a3cdc4-4f3a-ed26-02d6-6dbf6c1380d0": "Crimsonbeast Sheriff",
    "0eec6f2b-4d64-9c16-7846-b8865030f61c": "Kuronami Sheriff",
    "83778c03-45a3-67a2-3c89-6b8598327d58": "Ion Sheriff",
    "54337477-4aec-4a68-4673-7c8731639d30": "POLYfox Sheriff",
    "91d95358-4a3e-3abc-a251-98826225f18d": "POLYfrog Sheriff",
    "84589da8-4e2b-11bf-ca52-b88e6b7e1dbd": "Protocol 781-A Sheriff",
    "a5057a74-4a6a-561c-6974-d19a2b939599": "Lightwave Sheriff",
    "d26ce959-4ed2-7105-8f33-dea48e26de4a": "Random Favorite Skin",
    "2ba3ded8-47d5-58e3-1307-39800214636d": "Sentinels of Light Sheriff",
    "19b997bb-461a-fa85-250d-a8b0b8908fea": "Sakura Sheriff",
    "26ff0e3e-469a-cbdd-f79f-a3b89556cdef": "Peacekeeper Sheriff",
    "0568cd14-42ca-db85-3ac2-c485079bbbf1": "Schema Sheriff",
    "a40a6ce2-462c-c864-5d30-7b9408b98d3d": "Reaver Sheriff",
    "c0a39e8b-4d52-bfbc-21f2-a88b0f8c4856": "Mystbloom Sheriff",
    "1ef6ba68-4dbe-30c7-6bc8-93a6c6f13f04": "Standard Sheriff",
    "2e054476-4b48-ca0a-9c10-a38eab54eccc": "Cloudweaver Sheriff",
    "43e01e91-44d0-a819-852b-35b71673c648": "Sandswept Sheriff",
    "e8fd8fc3-40ce-3ed1-235a-1c8d9654874f": "Convex Sheriff",
    "42eaceac-46b2-eec0-2cca-10937761fe9e": "Varnish Sheriff",
    "9913da36-48b4-f0f5-db4e-43847a21e476": "Wasteland Sheriff",
    "121bc438-4748-b2ee-2c58-768c8c26838b": "Game Over Sheriff",
    "84d840c5-4479-4395-d823-e7acbe634c5e": "Arcane Sheriff",
    "bb0d20c6-415d-cf24-e738-0f99db6f9195": "Death Wish Sheriff",
    "b454bb93-4dd5-5a7c-6720-38afd82bfd78": "Sidekick Shorty",
    "4e98f273-472c-3376-7195-46a1f81402cc": "Araxys Shorty",
    "646e713f-4999-6c56-094c-dd9114bdb35a": "Neptune Shorty",
    "4c583a37-42d7-23db-5e38-1eafe96f2b9d": "Gaia's Vengeance Shorty",
    "0581fb92-4b2d-0ede-6bfc-8d93fde11f74": "Karabasan Shorty",
    "acedb6db-407b-5d62-9c27-07bbb2313fe3": "Rune Stone Shorty",
    "c9572061-4ee1-ff7d-b60c-ebac198d3706": "Prelude to Chaos Shorty",
    "9a37b09b-4768-b368-52ef-58ac62564637": "Doodle Buds Shorty",
    "da41a901-493c-80f7-955b-dfa0c69629fd": "Chromedek Shorty",
    "3a921c7b-4e8f-8543-bee8-01ba6da86874": "Hivemind Shorty",
    "15588213-4d09-344b-c7e1-28af37374c82": "Velocity Shorty",
    "1064fbd1-416c-bf00-0e30-a282a359847f": "Ruin Shorty",
    "4542410b-46ba-36f2-898d-c2815b504002": "Primordium Shorty",
    "7a3a9e66-4ac1-df74-193b-1984303f4f71": "Monarch Shorty",
    "5ebe29d1-46d9-03d6-825c-719e003d15ad": "Guardrail Shorty",
    "039207fd-4911-9d6b-b7ba-e3ade36ef77e": "Prism II Shorty",
    "1505ed97-4323-1a7b-7688-93a1e35e844f": "Aquatica Shorty",
    "310b80d8-4e1b-b4f0-b713-9dad458ce734": "Wunderkind Shorty",
    "fcb18a37-4a0d-ecd3-ee2c-c38496ed5ae2": "Genesis Shorty",
    "b36dad11-4105-6c08-0486-17ba96d0f2a4": "Oni Shorty",
    "9428e52d-4611-c8ff-1b63-7b8e386fe8cb": "Snakebite Shorty",
    "df0e23fe-4529-a9d5-c4c6-eaae086bda65": "Hue Shift Shorty",
    "075e4cf0-469b-25dc-8d6f-2995fbb093de": "Random Favorite Skin",
    "160d661d-4152-6914-8069-c393914759cb": "Sentinels of Light Shorty",
    "73ade1d7-47d1-680b-defe-268df2ad073b": "Transition Shorty",
    "48ad078a-4dae-2b85-a945-f4b6d1efecbb": "Standard Shorty",
    "a39bd1bb-4b17-4d57-c505-7eb15caffa4d": "Aerosol Shorty",
    "ae2ea89b-495e-2902-f67f-3490c1a03754": "Tilde Shorty",
    "b48639f6-4dbd-f0a3-8fd2-2a9d531fa6a0": "Cloudweaver Shorty",
    "7b51fc8a-4a5c-712e-c663-e6a7eeb61d91": "Tigris Shorty",
    "e917273f-42d1-3a8d-7c9e-54afd6e5e68d": "Wayfinder Shorty",
    "30635237-4877-4ea4-5ac4-239474d3a662": "Wasteland Shorty",
    "2e1936ed-4582-628f-da9c-25a7f47323cc": "RGX 11z Pro Operator",
    "a7f9dccd-43ad-0574-5d5f-1ab4950014e1": "Intergrade Operator",
    "4a1e0934-46ae-fa2a-a009-05ade5d43402": "VALORANT GO! Vol. 2 Operator",
    "6db556e4-4255-6c2c-6a80-8a9dfac96aa9": "Araxys Operator",
    "507330d3-4311-e010-183b-aba00a0705f1": "Radiant Entertainment System Operator",
    "8da0b49f-49cf-fc95-c4cb-2a90000ecc48": "MK.VII Liberty Operator ",
    "bdf1484c-44a7-2ef1-3d21-45b66ff8a89f": "Endeavour Operator",
    "17831113-4ff0-a6c9-0b20-6f9c077d74a2": "Origin Operator",
    "90ba4949-4a6a-cc54-efb2-3dbdbe1bf69c": "Striker Operator",
    "33aaa643-4bc4-4c5f-2762-228c7fc03949": "Red Alert Operator",
    "a491b943-43e3-4e98-64a6-fc87fca43605": "Glitchpop Operator",
    "b450a73d-431e-56b7-5b7f-67bddd38ee66": "Prelude to Chaos Operator",
    "d722313d-43cb-b38d-7841-75880a3ed2cb": "Elderflame Operator",
    "76f1d9e7-4675-6913-ca31-03a70815ee0e": "Imperium Operator",
    "44064b11-4e74-19c9-80a4-9f80875adaf5": "Nitro Operator",
    "c692e38e-4f38-0141-d0c9-aa99fab9362a": "Forsaken Operator",
    "279a54f8-4344-cd72-1d5b-15aa0e86a630": "Team Ace Operator",
    "93ccaf1f-4e44-0bc7-9ec4-ebab43f73d10": "Spitfire Operator",
    "341ef273-43fb-7911-71e8-50adada4cee1": "Infantry Operator",
    "5ced2c69-442e-d1ad-83fe-8fb8b2ac0c0f": "Prism Operator",
    "da025249-4217-6524-49a1-878c95095bd6": "Retrowave Operator",
    "9ffd45c4-4fa4-dca0-f46f-2d99ad1eae20": "K/TAC Operator",
    "403cce8c-4484-a796-a6f6-a0a07d9832e0": "Kohaku & Matsuba Operator",
    "201918d4-4c69-a91e-6a4f-6b86b084df1e": "Blush Operator",
    "64380fcd-43d2-5d91-dacb-f2becbfafb46": "Daydreams Operator",
    "cb07878f-484f-50dd-ab6b-5380640b13c5": "Iridian Thorn Operator",
    "0bd5da19-491f-dd4a-27e2-c9959b10a87a": "Luxe Operator",
    "7e831918-4580-5e2a-089a-84ad58fe1aae": "Magepunk Operator",
    "b2164926-4b85-852a-4bd7-d9bc27a642da": "Spline Operator",
    "a0a446f1-443d-3dc8-49c7-f2a70849f092": "Minima Operator",
    "1e9b6856-4aaa-4dba-1da7-3791690113d8": "Valiant Hero Operator",
    "83b49f36-4085-8179-6896-1a99f2d2d1d8": "Silvanus Operator",
    "de8d2ff4-49e0-c0a9-d29b-2da688220a01": "Genesis Operator",
    "7c7d116b-4e3d-c63e-23bb-69a5bd9198b9": "Libretto Operator",
    "bbf8ffb9-49c0-75c0-cc7d-8f8f03a4bd36": "Ion Operator",
    "b2783916-483a-9112-89c6-64b8d927b78c": "Cryostasis Operator",
    "acdd29aa-44b5-0d78-dc54-8f92ed555559": "Random Favorite Skin",
    "c21e2f34-4b8c-4350-33c8-a8b626ecaadc": "Gravitational Uranium Neuroblaster Operator",
    "b05c4c98-4108-e442-add7-da99a95a37b6": "Sentinels of Light Operator",
    "aecab890-43b7-d719-06bc-9295e3d116dc": "Reaver Operator",
    "e7ba6cec-495f-e08e-f8eb-6e90228bdf9e": "Tethered Realms Operator",
    "d47f9576-426f-4da3-761d-39967489550c": "Cavalier Operator",
    "d9a34604-42e9-3a01-a875-9293e08183a9": "Mystbloom Operator",
    "d1f2920f-469a-3431-ad96-96afbd0017f2": "Standard Operator",
    "5f260f34-4021-ab2c-8080-6287c4f9974b": "Aerosol Operator",
    "44175b4f-4503-4ce4-25fc-32a995d872c1": "Tilde Operator",
    "b53a990d-45c2-6212-a98f-b0aa5d6e6c23": "Tigris Operator",
    "ccb54094-4db8-2c9f-656b-f1bff329f469": "Convex Operator",
    "6558fd5d-4dc7-90f7-beea-ba9303551c3b": "Immortalized Guardian",
    "da29ce1e-43bb-c043-9cbc-34850517dc23": "RGX 11z Pro Guardian",
    "d8498f5f-4687-2eee-755e-00ae72f4ca94": "Intergrade Guardian",
    "2c32d9e3-42a1-7387-35ef-0c8eefacee1c": "VALORANT GO! Vol. 1 Guardian",
    "1082032a-4f20-12db-93ea-549332f91ddf": "Neptune Guardian",
    "abd5415f-4851-244f-4b8b-31af8e268822": "Gaia's Vengeance Guardian",
    "192f8546-487b-f47b-4779-c19972672fe8": "MK.VII Liberty Guardian",
    "04ccfe05-497c-2d52-2bd0-64a68955175e": "Spectrum Guardian",
    "16dba725-4de2-8412-c07f-af95c65db9a2": "Starlit Odyssey Guardian",
    "6141a40d-48cf-8466-6d46-558c0ff145ea": "Nebula Guardian",
    "97bc040f-44bb-cbb3-c9f4-3aa16d1c0655": "Abyssal Guardian",
    "00e6b758-448e-af3b-7dee-879aa4a51324": "Nitro Guardian",
    "2d5e6025-4166-730e-1024-abb766d19568": "Songsteel Guardian",
    "3ab36c94-4c91-d722-6f10-11bbbe382159": "Spitfire Guardian",
    "453a734b-4f14-9183-2be8-97b01f603368": "Ruin Guardian",
    "7422b876-443e-b975-faab-0ebf73dbc075": "Soulstrife Guardian",
    "acd76d4d-4d05-2597-d63b-12851b2b61ee": "Infantry Guardian",
    "06854a71-4eac-cb4c-cdbe-bbbdda492e9c": "Hydrodip Guardian",
    "2a049f35-4bcd-af25-21fd-ec942e2d5007": "Prime Guardian",
    "f9734048-446f-bb6f-0f58-f5aa6fded7c7": "Bubble Pop Guardian",
    "2700e91f-4201-5b8e-a9c7-b5aea72942e1": "Guardrail Guardian",
    "8966067d-4023-c88a-db56-2691f163d335": "Ruination Guardian",
    "f6dd8d93-4dbb-f7b2-d82a-41bfc8f46e31": "Blush Guardian",
    "80dbfa46-4a1f-c7a4-2e88-1499308c7b9a": "Magepunk Guardian",
    "da4317a0-4913-5e87-5b45-53be8e576481": "Tacti-Series Guardian",
    "26e675c5-46cc-65fb-7be2-db8a64dbde48": "Signature Guardian",
    "f097983d-4c5a-c7ed-c325-039c99bb824e": "Galleria Guardian",
    "b7931d66-4ca3-d67c-c130-6692c55ae26c": "Moondash Guardian",
    "850fea42-419f-f284-84ae-40ae1eabbb5b": "Oni Guardian",
    "1a38d03c-4114-6908-37dd-38a85d91cb2d": "9 Lives Guardian",
    "93309ef5-4f43-411a-5759-c794eb584c7c": "Aero Guardian",
    "96679876-4d41-683c-2e5c-2ea25ddd8fdf": "POLYfox Guardian",
    "23a16911-4cb1-2794-2d4c-3f99f1e2516b": "Jigsaw Guardian",
    "874025d8-4293-a38a-96ac-3d94954fb4b7": "Random Favorite Skin",
    "ee649b57-4811-332f-c484-aea45aada288": "Panoramic Guardian",
    "d75e69ae-4cde-2f43-8c3a-ac844e6ef1c9": "Silhouette Guardian",
    "74b9f0c4-4747-ab13-e3c4-3485b645beef": "Shellspire Guardian",
    "db348da1-49f2-0bad-b70a-e4ade9d31655": "Reaver Guardian",
    "77187a8f-4020-da44-a775-7a91ab814cdf": "Tethered Realms Guardian",
    "7122d78b-4e60-eb4d-5f65-738d7c1ce9ae": "Sovereign Guardian",
    "539e07ec-49b2-5f22-0d05-91b809229d64": "Recon Guardian",
    "cce860fd-4f64-7422-5c95-c7ad2cad0f15": "Infinity Guardian",
    "5d23dda7-405a-e903-4681-1a825146f028": "Reverie Guardian",
    "3bf1e8e0-47e8-f27a-6054-929575f41a54": "Standard Guardian",
    "14b17d97-4320-9b77-68a8-1ca7cfc0adae": "Fortune's Hand Guardian",
    "0a81818d-406e-1d8c-ce4d-9ba89dfdf1ab": "Ego Guardian",
    "b3cdf3a4-4547-f73a-f8aa-f390c1d3f42c": "Prism//Reloaded Outlaw",
    "2a86630c-4bb0-a9e3-69aa-0d96c788797f": "Aquatica Outlaw",
    "bd9c41dd-42b1-8555-78c1-81a36016bc03": "Random Favorite Skin",
    "740b9572-44b1-57bf-767e-6aa01811f94d": "Standard Outlaw",
    "9decabd1-4d9f-156d-4bea-4f973e57119f": "Cloudweaver Outlaw",
    "9fbeb60b-4c22-d736-b335-43ad53d0bc69": "Ego Outlaw",
    "a69950ce-460e-fa01-3b91-0ca6f9eac329": "Holomoku Outlaw",
    "774dee9a-4809-0e4d-4153-a883e908d4b2": "Task Force 809 Marshal",
    "95be56c3-4b3e-cc81-5fd6-b1af30448074": "Fiber Optic Marshal",
    "fc802ceb-4a39-39ac-adf5-02a812be2f8e": "Gaia's Vengeance Marshal",
    "8a5b92e4-4147-0d85-5e2c-d6a179645bec": "Composite Marshal",
    "db3bf2d9-449e-cd8a-950e-018ca893d404": "Rune Stone Marshal",
    "6250b40a-43a4-55d8-79d4-f6838d58151d": "Doodle Buds Marshal",
    "51da27fe-4a3f-016a-d18d-b68a47545f6f": "Songsteel Marshal",
    "fefdedbe-447d-b86a-b7dd-dab6d605cf6a": "Chromedek Marshal",
    "f037ea38-4be9-0f3d-003c-6f958a71e04b": "Venturi Marshal",
    "027a5d7f-4bfc-7c41-a012-24b8c6720fda": "Ruin Marshal",
    "d70d33ff-4a88-bf66-f256-bcb05fa9bd60": "Neo Frontier Marshal",
    "028c7b80-46ea-8f1d-3f7a-4c9c13a79977": "Monarch Marshal",
    "dd58ab43-4ff3-659e-8f30-b8bd26619d4d": "Avalanche Marshal",
    "fe297733-4ada-d817-dd7e-17b9cd1d62d5": "Black.Market Marshal",
    "6f48f7ff-40a5-cc9e-1320-bdaa388f5cbf": "Couture Marshal",
    "27ab5ed6-4614-d5c2-c53f-5391febe7099": "Magepunk Marshal",
    "542a3364-41c6-d030-d499-84bbecd72928": "Tacti-Series Marshal",
    "d4bcbc96-4be3-aa57-9a6a-11aecf60ac61": "Signature Marshal",
    "805722c4-4ac7-6179-7ce7-658b5f26d6ed": "Coalition: Cobra Marshal",
    "ad6309b5-4788-d401-33d0-4dbaeeadaf87": "Galleria Marshal",
    "af77e583-41fc-b0c2-3728-058d02502039": "Crimsonbeast Marshal",
    "43353883-446c-c2bf-5d44-298eb948ee80": "Moondash Marshal",
    "fb9ff2b0-4d71-d53c-364e-fe98fb5a2411": "Kuronami Marshal",
    "e64be1b4-4935-5215-874b-939d3b0ea57e": "Switchback Marshal",
    "6eea7984-4ca4-d547-4d50-b4a608072feb": "POLYfrog Marshal",
    "ad83a57d-414c-f714-a97f-99bad1128b2b": "Divine Swine Marshal",
    "4986a893-48a5-4c23-11f2-70bb9e9d284d": "Artisan Marshal",
    "48f218a6-42cf-4f63-0cda-39a5aef5d870": "Luna Marshal",
    "b273ade7-4971-c274-eb92-219ef6def086": "Premiere Collision Marshal",
    "457fe5d2-40c8-4490-6834-53a74e709f4a": "Random Favorite Skin",
    "5211efa8-4efd-09bb-6cee-72b86a8a5972": "Sovereign Marshal",
    "0dfc1800-4ddc-85fd-8382-32a2824135fa": "Reverie Marshal",
    "fd44b2d5-49ee-77ab-fa56-588f3ac0c268": "Standard Marshal",
    "9cba5b54-4d68-e13c-932e-4aac83e21e64": "Freehand Marshal",
    "dc0fd062-4658-519c-0c21-18a0943f123b": "Sandswept Marshal",
    "19f06522-40c8-8dc6-a0cd-92808b24751f": "Wasteland Marshal",
    "c31856f4-4ae1-cfb8-14cc-10a92b81e7c3": "Winterwunderland Marshal",
    "1c560472-4c65-616f-07e6-f98ad73c37c6": "Convergence Marshal",
    "e78fb82c-4800-e102-b7a6-33946fa2f199": "Task Force 809 Spectre",
    "91881981-4ce7-e081-a897-1bbb51996ac4": "Fiber Optic Spectre",
    "4f0c9544-469c-0c62-df2e-95b15d6f2333": "RGX 11z Pro Spectre",
    "646b7e79-4164-598c-56d1-c991d74ce695": "Intergrade Spectre",
    "89b78398-4c56-6371-cad7-8eb78ee3f550": "VALORANT GO! Vol. 1 Spectre",
    "55153919-4598-cb0f-4759-7ea546c6d121": "Neptune Spectre",
    "dbe2c9ea-41c4-522c-9204-dab09bac84d0": "Striker Spectre",
    "8cbd7b75-4759-08ee-fa0b-739bed1d1325": "Comet Spectre",
    "780a93e6-46aa-50c7-5e73-b885c5f6a141": "Radiant Crisis 001 Spectre",
    "1e473101-488a-e8ab-41cd-c6ad9d53443a": "Starlit Odyssey Spectre",
    "e655b7f1-499f-fcc9-fb44-20af54f3c701": "Emberclad Spectre",
    "3aebc432-4946-b9dc-ae50-59a6afa68c0d": "Abyssal Spectre",
    "0eab3e5c-4de4-e221-34fb-2ab435c89eb6": "Singularity Spectre",
    "5137dacb-4df6-b513-765b-96b9ecfc435c": "Sarmad Spectre",
    "d405272b-4388-578c-e33b-04842496b8c1": "Hivemind Spectre",
    "35469802-4ae2-f86a-dfaa-d484cc29481e": "Venturi Spectre",
    "a786ea8f-42f2-ae5f-376f-2bb66df1a62f": "Forsaken Spectre",
    "6196c91c-4f0a-2aa2-342a-6fbac6d4ec3c": "Velocity Spectre",
    "95ca4d2b-4166-8e0e-8d79-d79957f58b81": "Soulstrife Spectre",
    "b160a897-4b92-0034-58ff-2b9b8c2d7340": "Primordium Spectre",
    "8d4d74c3-4771-52a3-b3eb-a38cc0222643": "Infantry Spectre",
    "eb9ec7c9-4c20-e702-81c7-63bbe165aa12": "Horizon Spectre",
    "20807bd8-4259-35e5-e54e-c1b214f58cc8": "Prime Spectre",
    "a0938d46-4593-19b4-1aa5-f3b32ecb9963": "Avalanche Spectre",
    "b9836020-433a-ace4-eb35-3fbd67688c53": "Prism Spectre",
    "4643050b-417c-0d84-3626-27b709c49c67": "Serenity Spectre",
    "f9c2e823-4eeb-d872-8a4c-d5a0bf8a3b6c": "Ruination Spectre",
    "30b19f29-419b-1adc-3561-40be2b1f7841": "Kingdom Spectre",
    "8badce8c-4239-34a5-a23d-6595689df562": "Blush Spectre",
    "bdb396b1-49eb-851c-b107-1ea2027cab26": "Monstrocity Spectre",
    "3eb4d837-4ae9-b52a-b41d-2789f9974f15": "Luxe Spectre",
    "a3f8e1b3-4654-f3ea-15ba-9eb9fd6a0b0d": "Magepunk Spectre",
    "418ef9fe-4675-6620-3755-c19aca3ff131": "Spline Spectre",
    "2d28e21f-4986-650d-70bd-a2927a0e337b": "Minima Spectre",
    "f743fe2f-4cab-71d9-81e2-5b8f2f52923f": "Kuronami Spectre",
    "eacea54e-4e53-2715-cd4a-5d860aa68449": "Ion Spectre",
    "ed78f73b-4055-2bd2-7cd6-a1ae7e9025c5": "Hue Shift Spectre",
    "fbaedf2b-4a8b-1949-ddaa-27ab3f6d8ae4": "Aero Spectre",
    "9042279e-4491-1a01-a346-928f89f01ea7": "POLYfrog Spectre",
    "eaa73ab9-4688-0c40-09ad-85b535a50723": "Protocol 781-A Spectre",
    "f45824e7-4573-d473-0e70-959b76fc4dab": "Luna Spectre",
    "c79318a6-4ffd-a99f-f452-77947640f688": "Random Favorite Skin",
    "4a8e8ff6-44f2-0ebf-6fa8-a5af76b628ee": "Gravitational Uranium Neuroblaster Spectre",
    "7c232164-4b8c-7a8f-7ae5-42987cbfb14f": "Sentinels of Light Spectre",
    "91918349-4475-f56b-dc5a-e8bd3e630660": "Shellspire Spectre",
    "1cb1ab52-4c7d-0775-77f4-eaac99968261": "Reaver Spectre",
    "26b1c794-4370-f354-ff4d-3a8b95edff79": "Recon Spectre",
    "53ab2a6a-46c5-32b9-e045-6781e677d7ff": "Infinity Spectre",
    "f01d1307-4299-42f5-2c5e-7dab7e69ab19": "Standard Spectre",
    "fb3f3ffd-46bc-41e3-25c9-2688f2d017ed": "Evori Dreamwings Spectre",
    "70f4a686-42e0-5800-b09b-8cbce7fc2f8d": "Freehand Spectre",
    "910991b7-40de-183d-12ea-d99e67cfa910": "Tigris Spectre",
    "ddbead4d-40b1-afe4-e44f-eca9e2022458": "NO LIMITS Spectre",
    "e22a30b2-413b-e194-3cd6-47b20b825feb": "Sandswept Spectre",
    "c8a5ba23-4f0d-c7de-8e2f-c184e2fc27ba": "Convex Spectre",
    "b4e5bb69-4e12-113f-c43b-efa5b13cb96d": "BlastX Spectre",
    "f7da43d8-450b-a03f-ceb7-c4b20f738392": "Wasteland Spectre",
    "66a6a6a1-44c7-beac-0b67-54aaa8243367": "Immortalized Stinger",
    "282c15e6-4372-2f18-9143-2d9cdd942c4c": "RGX 11z Pro Stinger",
    "42da0f19-4017-5cb8-08a4-368315561fdf": "Aristocrat Stinger",
    "cebd9a89-4ef1-48fa-6c4e-6bbc1cdd1be8": "Composite Stinger",
    "6e507ef4-4e78-e3ed-11c1-0397b94f4cfc": "Tactiplay Stinger",
    "0cf70376-4150-39aa-5657-8890617bc0d1": "Red Alert Stinger",
    "5a4a0ea0-4ac6-d130-c917-45a7bb89ae42": "Prelude to Chaos Stinger",
    "9444ba80-4ae7-985d-40a2-2788f96dd544": "Doodle Buds Stinger",
    "0a128cb6-4bbb-f618-85cb-82bbd17bcbb1": "Surge Stinger",
    "3fc40900-4d9d-c22f-c0f6-e0b53827ef83": "Shimmer Stinger",
    "bf7e260f-407e-9e16-e47e-ba921c10f046": ".SYS Stinger",
    "338e3ee3-4927-733f-32b6-bcac795d23ac": "Prism II Stinger",
    "5740a0f6-4f9a-c38b-db63-1a935e4bad92": "Aquatica Stinger",
    "598bb272-4bfd-ae82-0242-6490cc6f721e": "Couture Stinger",
    "cfbcbbcb-4d51-94cb-2efb-9fbb0d655b45": "Signature Stinger",
    "7fa8b218-4943-e745-f62f-a9b666bdc10b": "Overdrive Stinger",
    "847fe9da-45cc-21d4-0138-7aa4d8b31d8e": "Silvanus Stinger",
    "92f1dd4b-47f5-2088-9370-f89857962bc2": "Moondash Stinger",
    "2b7f65f7-4e85-becc-5f3d-39961f937b79": "Libretto Stinger",
    "cfca617a-4240-377f-ed3f-778fa63729ed": "Switchback Stinger",
    "9d7ed392-4c4c-b1c4-7232-3cbb07b2e133": "Sensation Stinger",
    "d25dfdc4-4fce-e121-88ef-66b5dadeee09": "Random Favorite Skin",
    "1cd6f578-483b-37a1-a7ef-9a907fac416a": "Sakura Stinger",
    "46c8b165-4ba5-d42c-79e9-4fba8951ca48": "Schema Stinger",
    "3d6eb464-4193-a8c6-5aff-d593520163b3": "Lycan's Bane Stinger",
    "7858961c-47ae-f109-2f70-f0b78ea99aaf": "Transition Stinger",
    "8fb27bb1-4080-581d-bcd3-53ae01861654": "Sovereign Stinger",
    "51e2b876-4339-521d-8d68-9aaec119bc1f": "Cavalier Stinger",
    "940fb417-4a9c-3004-41f5-3e8f1f4178b2": "Standard Stinger",
    "3760761d-4be6-bc25-d9a8-a0b9137651fd": "Gridcrash Stinger",
    "86d41080-4b1f-046e-6736-148539e76df7": "Cloudweaver Stinger",
    "e1297b8f-4374-3131-27a9-38bb0eda1c0d": "Depths Stinger",
    "8fe5ebbc-4ce7-a248-9766-288441706e0a": "Ego Stinger",
    "26fbcf26-4135-b8e3-277e-8a9c27e3d34d": "Varnish Stinger",
    "e1888a19-4ad6-e406-0002-0bb1ad411168": "Convergence Stinger",
    "58442f45-4783-42a2-f4cb-789a27555889": "Task Force 809 Knife",
    "9fb366b6-46df-a722-0cf2-9c9b85936f17": "RGX 11z Pro Blade",
    "03de6b1a-4497-72e8-ae0c-2984b2e7e2b9": "RGX 11z Pro Firefly",
    "1bc43715-4679-3f9d-ffc1-d69b373407cc": "Altitude Knuckle Knife",
    "c5482640-4652-6948-29c6-769e8198db27": "Xenohunter Knife",
    "050aa35d-41b7-241c-d0b5-23b53ab0769a": "Intergrade Blade",
    "9103fdf7-4361-5ac5-37ae-7cb51f13f45d": "VALORANT GO! Vol. 1 Knife",
    "d034911c-45a6-1ce4-e6f5-4cbe57e9d4f1": "Yoru's Stylish Butterfly Comb",
    "a486efac-4415-1bfa-68d1-19bca9968101": "Araxys Bio Harvester",
    "c3f1c9d6-441b-7def-1bf2-2c82719a4de8": "Neptune Anchor",
    "f0ba8044-4964-ba1f-7f0f-e68dc2118d42": "Power Fist",
    "f91a1dd8-4f5f-bce4-f01d-4da95322c485": "Gaia's Wrath",
    "4fc1bb49-4847-7262-8cfe-fcaf0f62f0d1": "Gaia's Fury",
    "c4cb8c3b-4cb8-0260-609b-9a922a817a8f": "MK.VII Liberty Combat Knife",
    "400bb847-4f4f-a39e-cd52-589f00b2204f": "Waveform",
    "8330a4c0-4e98-1cb7-9695-6b998b77138d": "Obsidiana",
    "093e3c69-4e14-6f75-1ee4-fc92efb91f9a": "Composite Knife",
    "1ea64c8d-43c4-fce8-7354-01bdd6c0ee17": "Champions 2021 Karambit",
    "6946cd0e-4e4a-ec4f-9238-dfb71715722b": "Champions 2022 Butterfly Knife",
    "27f27500-491c-32d4-1db6-1f85e479c103": "Champions 2023 Kunai",
    "ac687fc4-40c5-4c41-6a7c-5eb59adabd60": "Origin Crescent Blade",
    "31309f0b-49cd-295c-490d-96821a21c72f": "Striker Knife",
    "3562e143-49eb-08be-2d0a-98a1f06fb7bd": "Comet Sword",
    "71020826-483d-34f8-8da7-928f87942c10": "Radiant Crisis 001 Baseball Bat",
    "a4c41553-4ba5-efee-5685-7a9f0cdf7878": "Nebula Knife",
    "c91e4850-4d32-3b12-f411-3e9f644ea616": "Hack",
    "ddc025b2-475f-889a-2800-80b4215582bc": "Glitchpop Dagger",
    "f0c42e14-4a92-132d-dfd4-cbbef103340c": "Glitchpop Axe",
    "1b8de6d7-4f37-7170-acd7-e78829f7959a": "Terminus A Quo",
    "4b66c44e-4b97-aa19-5c9c-fe837abaa95a": "Emberclad Hammer",
    "cd6ce089-43fa-c4dc-3f8f-0391cb604b5d": "Caeruleus",
    "6e0496c1-4c98-7abe-16c4-7ca3653e5cd8": "Blade of Chaos",
    "94b40026-4efb-39ea-69d7-fca60be39c56": "Elderflame Dagger",
    "d7eaba36-4f20-9685-7c5a-dabe6d31d81c": "Blades of Imperium",
    "151ee26c-4e82-e7ca-dad1-099e7fb34774": "Singularity Knife",
    "6417e12d-4f03-13d4-8704-20bf3a1bcb5b": "Blade of Serket",
    "45129867-4977-e2a5-bead-cb828101b623": "Songsteel",
    "1f81e40e-460a-75fd-fb38-5f90b6fbb596": "Chromedek Gauntlet",
    "9a98f7dd-426c-603e-0569-e9b317c25ee4": "VCT LOCK//IN Miseric\u00f3rdia",
    "24cf2882-48c7-f287-155a-a4b6b083baa4": "Hivemind Sword",
    "2640e9a6-415f-4c3e-cac0-16a24edb41c0": "Venturi Knife",
    "ed792f00-43a7-cc88-b64b-b78c9de399a1": "Forsaken Ritual Blade",
    "ccde2f25-4525-ef52-e1f0-bd88184bd4a4": "Velocity Karambit",
    "9c350ebe-458b-e6ed-ab77-2fb00cf249c1": "Ruin Dagger",
    "c8b926df-4554-1b07-5a43-a9850bafca96": ".SYS Melee",
    "cdcfab50-425d-6410-7a54-6aa913b7ce48": "Neo Frontier Axe",
    "dfe96f5a-4be0-c3f4-8e31-7f962bca2ade": "Soulstrife Scythe",
    "3e633a9a-482a-30fb-90da-059ff6cd400b": "Blades of Primordia",
    "e100dff1-4cf5-54ec-aa65-6fadbc22973b": "Prime Axe",
    "9237e734-4a2a-38ae-7438-6cbee901877d": "Prime//2.0 Karambit",
    "dc6cb084-4fb2-89cf-2113-4facb7767e9f": "XER\u00d8FANG Knife",
    "2887c565-4c82-842d-b1ca-5682ddb88ffd": "Bubble Pop Light Stick",
    "908be835-43bc-b728-35a4-0fa91f612cc0": "Outpost Melee",
    "4ef258bb-49bf-74c5-3405-16a041cb7306": "Guardrail Hammer",
    "9b6d0e3d-43eb-e9d5-4069-2194e02d6e6e": "Black.Market Butterfly Knife",
    "82fbfa4c-4bac-a6da-c5ed-00898e83637f": "Bound ",
    "6fa830c2-4924-87b2-1510-2fa4fbdca1db": "Prism Knife",
    "0c07c7f3-4532-bc57-d474-26b3b39a38e6": "Prism III Axe",
    "b1e9530d-4618-4f2e-1b75-f1a90c91b19e": "Broken Blade of the Ruined King",
    "f82aa022-4a6c-fa40-105d-92af6510ae1b": "Kingdom Knife",
    "83e8641b-41d0-821d-5eeb-5999e9294a0c": "K/TAC Blade",
    "2e4300f9-49b3-6bbe-af7c-94a6f56ff12e": "Equilibrium",
    "fcf7417a-4b58-b09d-c557-6185acaf7425": "Blade of Aemondir",
    "46163791-47b9-2ef0-d255-aaa5146051bb": "Smite Knife",
    "80735f79-4eeb-76d4-f390-88898e819d76": "Daydreams Crowbar",
    "8e760310-4d95-354b-a910-049eaa4d2fc6": "Catrina",
    "16da5cca-49bc-2516-8ee6-c98d93e2d911": "Iridian Thorn Blade",
    "7d45aaad-4ac9-77b1-e7ca-3991be5721dd": "Celestial Fan",
    "4af88517-4949-9caa-9dda-1980f07202a4": "Luxe Knife",
    "c18e781e-40a0-80e6-256a-54ae7355e7eb": "Magepunk Electroblade",
    "59f627f1-42f3-670d-5323-3499c2913289": "Magepunk Shock Gauntlet",
    "6029ac35-4eca-8428-26d5-0896013e4c63": "Magepunk Sparkswitch",
    "f6cfd500-4eab-3c1d-9eeb-188e90731692": "Spline Dagger",
    "62a52d27-4c08-104c-3bd0-22be86848cc3": "Ruyi Staff",
    "6bea8564-48a8-5011-dbf7-a2856713de08": "Overdrive Blade",
    "ec04e1a4-4067-bb9c-c18b-46a80e5f3f1f": "Crimsonbeast Hammer",
    "3209e2af-4703-088b-ebef-8da89b4cef87": "Genesis Arc",
    "e37229ed-4ddf-5e7e-e744-8fba60fa2c37": "Kuronami no Yaiba",
    "46664f5b-49ca-3e09-4fe5-56bdef536335": "Ion Energy Sword",
    "a590c03a-43b1-a408-4c6b-0bb9fdda1570": "Ion Karambit",
    "206fc3fe-45a0-6c19-c367-229b98b6a2aa": "Oni Claw",
    "4e7342a5-4820-2d79-a488-0fa51a4357f7": "Onimaru Kunitsuna",
    "729b8a6a-47e9-ec6a-67ef-068814d1f7d6": "Switchback Ascender",
    "feb4eb97-4ab3-793a-9a92-1b8af59dc023": "Cryostasis Impact Drill",
    "c39f405f-42f1-acd1-a350-d3af39c32e33": "Artisan Foil",
    "239ed20b-479c-e08e-c4b5-6ba0394576d4": "Personal Administrative Melee Unit",
    "07409307-46cc-98db-ec92-ceb04a865f73": "Luna's Descent",
    "b5f42a00-425a-6fdf-61af-bb9a564c3d79": "Random Favorite Skin",
    "0357caf1-41a9-cb1c-c080-38aab13d9a7e": "Gravitational Uranium Neuroblaster Baton",
    "d78eef32-4531-0f68-f2d2-d28c52ecea38": "Orion Sword",
    "6fd8cc46-48b3-f02c-46e3-cba372e7a328": "Relic of the Sentinel",
    "a03598b3-4879-3380-eb4c-d6b2d29dd565": "Relic Stone Daggers",
    "2da73e96-46e9-7161-531b-54a293acc4f2": "Shellspire Sword",
    "4e2fd704-4372-a082-8423-c4a1da4d62f1": "Transition Knife",
    "52a1647c-42d9-b40e-16cf-a7821566ad81": "Snowfall Wand",
    "0aecb2b8-49cc-560e-42c7-6cbce44f05cf": "Reaver Knife",
    "b73d7b16-4652-bc5b-5c4c-068aabb19d0a": "Reaver Karambit",
    "f4e40444-43f3-e6f7-3271-bdb7d1492b05": "Prosperity",
    "2e77ac95-4681-3d87-bbdc-93a50ff6b1f6": "Sovereign Sword",
    "95938baf-4000-1b9a-42e2-77909a49d380": "Eternal Sovereign",
    "39cf499b-4f82-e875-5320-b0a1d7fc58d4": "Recon Balisong",
    "4f6033d5-4b24-94f0-31ab-f6969a2c926c": "Titanmail Mace",
    "516e0013-480b-6c1f-b05a-b6b616bffbfc": "Mystbloom Kunai",
    "5b95aba8-4223-e937-3ab7-9995c9e3064b": "Reverie Sword",
    "12cc9ed2-4430-d2fe-3064-f7a19b1ba7c7": "Melee",
    "ccc98dd6-4957-ee80-1489-c5889d128261": "Evori's Spellcaster",
    "be489303-4aa4-ba46-e6a8-02ae4c7a7b3a": "Tilde Knife",
    "5de8dd22-41f1-381b-e138-b1a1c206c8fc": "Fortune's Scepter ",
    "5724cd18-458b-af3d-b60a-239c5a8c081a": "Hu Else",
    "b6d1788f-4ef6-6b05-3650-43bd455ba744": "NO LIMITS Bat",
    "9aaeb22b-47e4-8a4b-ed37-0c9bf6b1dad1": "Sandswept Dagger",
    "5844ccd5-4a8d-e84d-b5b1-dfaaa8f34d84": "BlastX Polymer KnifeTech Coated Knife",
    "c52fe5d7-4500-ffc0-cbcd-bfa29b7ea040": "Ego Knife",
    "ce1a391f-4819-dc71-8a23-0e95b0b79aef": "Kaimana",
    "1cd09fbd-43cb-a5f6-90fa-08994342d747": "Ignite Fan",
    "e49c0fd2-435c-2c41-9164-4996080f455b": "Winterwunderland Candy Cane"
}

allModes = {
    "96bd3920-4f36-d026-2b28-c683eb0bcac5": "Standard",
    "a8790ec5-4237-f2f0-e93b-08a8e89865b2": "Deathmatch",
    "a4ed6518-4741-6dcb-35bd-f884aecdc859": "Escalation",
    "e086db66-47fd-e791-ca81-06a645ac7661": "Team Deathmatch",
    "d2b4e425-4cab-8d95-eb26-bb9b444551dc": "Onboarding",
    "4744698a-4513-dc96-9c22-a9aa437e4a58": "Replication",
    "e921d1e6-416b-c31f-1291-74930c330b7b": "Spike Rush",
    "e2dc3878-4fe5-d132-28f8-3d8c259efcc6": "The Range",
    "57038d6d-49b1-3a74-c5ef-3395d9f23a97": "Snowball Fight",
    "5d0f264b-4ebe-cc63-c147-809e1374484b": "Swiftplay"
}

allRanks = ["UNRANKED", "Unused1", "Unused2", "IRON 1", "IRON 2", "IRON 3", "BRONZE 1", "BRONZE 2", "BRONZE 3", "SILVER 1", "SILVER 2", "SILVER 3", "GOLD 1", "GOLD 2", "GOLD 3", "PLATINUM 1", "PLATINUM 2", "PLATINUM 3", "DIAMOND 1", "DIAMOND 2", "DIAMOND 3", "ASCENDANT 1", "ASCENDANT 2", "ASCENDANT 3", "IMMORTAL 1", "IMMORTAL 2", "IMMORTAL 3", "RADIANT"]


#FOR ENTRIESE THAT ARE ALL ZERO, maybe make the multipliers 1 instead of 0
mapCoords = {
    "Ascent": {
        "xMultiplier": 7e-05,
        "yMultiplier": -7e-05,
        "xScalar": 0.813895,
        "yScalar": 0.573242
    },
    "Split": {
        "xMultiplier": 7.8e-05,
        "yMultiplier": -7.8e-05,
        "xScalar": 0.842188,
        "yScalar": 0.697578
    },
    "Fracture": {
        "xMultiplier": 7.8e-05,
        "yMultiplier": -7.8e-05,
        "xScalar": 0.556952,
        "yScalar": 1.155886
    },
    "Bind": {
        "xMultiplier": 5.9e-05,
        "yMultiplier": -5.9e-05,
        "xScalar": 0.576941,
        "yScalar": 0.967566
    },
    "Breeze": {
        "xMultiplier": 7e-05,
        "yMultiplier": -7e-05,
        "xScalar": 0.465123,
        "yScalar": 0.833078
    },
    "District": {
        "xMultiplier": 0,
        "yMultiplier": 0,
        "xScalar": 0,
        "yScalar": 0
    },
    "Kasbah": {
        "xMultiplier": 0,
        "yMultiplier": 0,
        "xScalar": 0,
        "yScalar": 0
    },
    "Drift": {
        "xMultiplier": 0,
        "yMultiplier": 0,
        "xScalar": 0,
        "yScalar": 0
    },
    "Piazza": {
        "xMultiplier": 0,
        "yMultiplier": 0,
        "xScalar": 0,
        "yScalar": 0
    },
    "Abyss": {
        "xMultiplier": 8.1e-05,
        "yMultiplier": -8.1e-05,
        "xScalar": 0.5,
        "yScalar": 0.5
    },
    "Lotus": {
        "xMultiplier": 7.2e-05,
        "yMultiplier": -7.2e-05,
        "xScalar": 0.454789,
        "yScalar": 0.917752
    },
    "Sunset": {
        "xMultiplier": 7.8e-05,
        "yMultiplier": -7.8e-05,
        "xScalar": 0.5,
        "yScalar": 0.515625
    },
    "Pearl": {
        "xMultiplier": 7.8e-05,
        "yMultiplier": -7.8e-05,
        "xScalar": 0.480469,
        "yScalar": 0.916016
    },
    "Icebox": {
        "xMultiplier": 7.2e-05,
        "yMultiplier": -7.2e-05,
        "xScalar": 0.460214,
        "yScalar": 0.304687
    },
    "The Range": {
        "xMultiplier": 0,
        "yMultiplier": 0,
        "xScalar": 0,
        "yScalar": 0
    },
    "Haven": {
        "xMultiplier": 7.5e-05,
        "yMultiplier": -7.5e-05,
        "xScalar": 1.09345,
        "yScalar": 0.642728
    }
}




DBUG = False #set to true to unleash the debug statements
if DBUG:
    dbug_print = print
else:
    dbug_print = lambda *args, **kwargs: None
#============================================================================================================






#============================================================================================================
#ensures that we dont exceed the max requests. write this after every API request!!!!!
def limit_check(response):
    print("\t\t\trequest made.")
    print(f"\t\t\t\tAlleged requests made: [{response.headers['x-ratelimit-limit']}]/30")
    if(int(response.headers['x-ratelimit-limit']) >= 30):
        print(f"\t\t\t\tsleeping for [{response.headers['x-ratelimit-reset']} + 2] sec")
        time.sleep(int(response.headers['x-ratelimit-reset']) + 2)     

#ALL API REQUESTS SHOULD LOOK LIKE THIS
#       print("Making request...")
#       response = <API request statmement>
#       limit_check(response)
#============================================================================================================






#============================================================================================================
#FUNCTION DEFINITIONS(you can collapse)
#These all directly access API which is why theyre here

#Accesses API
#returns puuid of player
def get_puuid(name: str, tag: str, api_key: str):

    url = f"https://api.henrikdev.xyz/valorant/v1/account/{name}/{tag}"
    headers = {'Authorization': f'{api_key}'}

    print("Making request...")
    response = requests.get(url, headers=headers)
    limit_check(response)



    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch puuid: {response.status_code}")
        error = response.json()['errors'][0]['message']
        details= response.json()['errors'][0]['details']
        code = response.json()['status']
        if details == "null":
            details = ""     
        else:
            details = f"Details: {details}"
        response_message = f"{error} Code:{code}....{details}"
        print(response_message, "\nEXITING PROGRAM")
        quit()

#Accesses API
#returns the player's raw data match history
#format is here: https://valapidocs.techchrism.me/endpoint/match-history 
def get_raw(puuid: str,api_key: str,queue: str, startIndex: int, endIndex: int):
    url = f"https://api.henrikdev.xyz/valorant/v1/raw"
    headers = {
        'Authorization': f'{api_key}',
    }
    body = {
        "type": "matchhistory",
        "value": puuid,
        "region": "na",
        "queries": f"?startIndex={startIndex}&endIndex={endIndex}&queue={queue}"
    }
    
    print("Making request...")
    response = requests.post(url, headers=headers, json=body)
    limit_check(response)

 
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch raw_data: {response.status_code}")
        error = response.json()['errors'][0]['message']
        details= response.json()['errors'][0]['details']
        code = response.json()['status']
        if details == "null":
            details = ""     
        else:
            details = f"Details: {details}"
        response_message = f"{error} Code:{code}....{details}"
        print(response_message, "\nEXITING PROGRAM")
        quit()

#Accesses API
#returns match details of matchID
#format is here: https://valapidocs.techchrism.me/endpoint/match-details 
def get_match_details(matchID: str,api_key: str):
    url = f"https://api.henrikdev.xyz/valorant/v1/raw"
    headers = {
        'Authorization': f'{api_key}',
    }
    body = {
        "type": "matchdetails",
        "value": matchID,
        "region": "na",
    }
    
    
    print("Making request...")
    response = requests.post(url, headers=headers, json=body)
    limit_check(response)
 
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch raw_data: {response.status_code}")
        error = response.json()['errors'][0]['message']
        details= response.json()['errors'][0]['details']
        code = response.json()['status']
        if details == "null":
            details = ""     
        else:
            details = f"Details: {details}"
        response_message = f"{error} Code:{code}....{details}"
        print(response_message, "\nEXITING PROGRAM")
        quit()
#==========================================================================================================





#============================================================================================================
#READ THIS                                   
#FUNCTION DEFITIONS (you can collapse all of these)
#these access and save data


#Does not access API
#auxillary function for the get_data functions
#returns the new team configuration(flips teams)
#team_side is either string or dict, depending on if we are analyzing individual player or all player
def switch_teams(team_side):
    dbug_print("---SWITCHING TEAMS---")
    if isinstance(team_side, dict):

        for key, value in team_side.items(): #allplayer analysis
            if value['Side'] == "Attack":
                team_side[key]['Side'] = "Defense"
            elif value['Side'] == "Defense":
                team_side[key]['Side'] = "Attack"

    elif isinstance(team_side, str): #player analysis

        if team_side == "Attack":
            team_side = "Defense"
        else:
            team_side = "Attack"

    else:
        print("team_side has type ", type(team_side))
        raise ValueError("Invalid team side")

#Does not access API
#auxillary function for analyze_match
#mutates output_dict, does it for specific player
def get_data_for_player(curr_match: dict, map_name: str, puuid: str, output_dict: dict):
    
    player_team = next((player['teamId'] for player in curr_match['players'] if player['subject'] == puuid), None)
    if player_team == "Red": #if player_team is None, player was not found
        team_side = "Attack"
    elif player_team == "Blue":
        team_side = "Defense"



    round_count = 0
    kill_array_index = 0
    for round_result in curr_match['roundResults']:
        if kill_array_index < len(curr_match['kills']): #as long as there are still kills to be checked, we continue
            dbug_print("\n")
            
            round_count += 1
            dbug_print('currently examining new round [', round_count, "]")
            dbug_print('  player is on ', team_side)

            if round_count > 24 or ( round_count % 12 == 1 and round_count > 1):  #switch teams when needed(after round 12,and in OT)  *not explicitly tested to be correct
               
                switch_teams( team_side)


                
        
            #get specified player's stats
            for player_stat in round_result['playerStats']:
                if player_stat['subject'] == puuid:
                    dbug_print("\tplayer stats found")
                    curr_round_stats = player_stat
                    break
            
            #location data will need these things
            loadout_value = curr_round_stats['economy']['loadoutValue']
            weapon = allGuns[curr_round_stats['economy']['weapon']]
            armor  = allArmor[curr_round_stats['economy']['armor']]



            #determine where to put the next entry in the array by loadout value
            array_spot = (int)(loadout_value/50)
            dbug_print("\tloadout value[", loadout_value, "]->array spot[", array_spot, "]")
        
        
        #calculate round length

            #calculate start time 
            round_start_time = curr_match['kills'][kill_array_index]['gameTime'] - curr_match['kills'][kill_array_index]['roundTime']
            
            #calculate start time of next round, if there is no next round, time = -1
            next_round_start_time = -1
            for kill_info in curr_match['kills']:
                if kill_info['round'] == round_count + 1:
                    next_round_start_time = kill_info['gameTime'] - kill_info['roundTime']
                    break
        

            #subtract the buy phase time
            buy_phase = 0
            if(round_count == 1 or round_count == 13 or round_count == 25):
                buy_phase = 45000
            else:
                buy_phase = 30000

            if(next_round_start_time == -1):
                round_length = curr_match['matchInfo']['gameLengthMillis'] - round_start_time #might be wrong because gameLengthMillis might not start from the start of round 1
            else:
                round_length = next_round_start_time - round_start_time - buy_phase
        #round length calculated
        
            dbug_print('\t\tround start(ms)  = ', round_start_time)
            dbug_print('\t\tnext round start(ms)  = ', next_round_start_time)
            dbug_print('\t\tbuy phase(ms)    =', buy_phase)
            dbug_print("\t\tround length(ms) = ", round_length)



            
            #loop through all kills in the current round
            while(kill_array_index < len(curr_match['kills']) and curr_match['kills'][kill_array_index]['round']+1 == round_count):
                dbug_print('\t\t\tcurrently examining kills on round ', curr_match['kills'][kill_array_index]['round']+1, 'should match ', round_count)
                curr_kill_info = curr_match['kills'][kill_array_index]

                if(curr_kill_info['victim'] == puuid):#our player died!

                    death_time_percentage = (int)(round(curr_kill_info['roundTime']/round_length, 2)*100)
                    dbug_print("\t\t\t\tdeath_time[0,100]: ", death_time_percentage, "%")#DBUG

                    #GET RID OF STUPID ISO ULT DATA
                    if abs(curr_kill_info['victimLocation']['x']) <= 20000 and abs(curr_kill_info['victimLocation']['y']) <= 20000:
                        
                        dbug_print('\t\t\t\tINSERTING death INTO SLOT: [', array_spot, "]")
                        output_dict[map_name][team_side]['death_info'][array_spot].append({

                            'Location': {'x': curr_kill_info['victimLocation']['x'], 'y':curr_kill_info['victimLocation']['y']},
                            'Armor' : armor,
                            
                        })

                    #add to the death time
                    output_dict[map_name]['All_Death_Times'][death_time_percentage]+=1
                
                if(curr_kill_info['killer'] == puuid):#our player got a kill!
                    
                    kill_time_percentage = (int)(round(curr_kill_info['roundTime']/round_length,2)*100)
                    dbug_print("\t\t\t\tkill_time[0,100]: ", kill_time_percentage, "%")#DBUG

                    #add kill info (a bit more complicated)
                    for player_loc in curr_kill_info['playerLocations']:

                        if player_loc['subject'] == puuid:

                            #GET RID OF STUPID ISO ULT DATA
                            if abs(player_loc['location']['x']) <= 20000 and abs(player_loc['location']['y']) <= 20000:
                                
                                dbug_print('\t\t\t\tINSERTING kill INTO SLOT: [', array_spot, "]")
                                
                                #add datapoint to output
                                output_dict[map_name][team_side]['kill_info'][array_spot].append({
                                    'Location': {'x': player_loc['location']['x'], 'y': player_loc['location']['y']},
                                    'ViewRadians': player_loc['viewRadians'],
                                    'Weapon': weapon
                                })
                            break
                            

                    #add to the kill time
                    output_dict[map_name]['All_Kill_Times'][kill_time_percentage]+=1
                


                kill_array_index += 1

# UNFINISHSED
#Does not access API 
#auxillary function for analyze_match
#mutates output_dict, different algorithm for all players
def get_data_for_all_players(curr_match: dict, map_name: str, output_dict: dict):
    

    all_players_stats = {player['subject']: {"Side": "Attack" if player['teamId'] == "Red" else "Defense" if player['teamId'] == "Blue" else "MISSING_DATA", "Loadout_Value": None, "Weapon": None, "Armor": None} for player in curr_match['players']}
    round_count = 0
    for round_result in curr_match['roundResults']:
        round_count += 1

        dbug_print('\tcurrently examining new round [', round_count, "]")

        if round_count > 24 or ( round_count % 12 == 1 and round_count > 1):  #switch teams when needed(after round 12,and in OT)  *not explicitly tested to be correct
            switch_teams( all_players_stats)

        #get all the players buy values, weapons, armor (this may not be very effective, because we are getting all this info for players even if they didnt get a kill this round)
        dbug_print("\t\tgetting all player economies")
        if round_result['playerEconomies'] is not None and isinstance(round_result['playerEconomies'], list):
            for curr_player_economy in round_result['playerEconomies']:
                all_players_stats[curr_player_economy['subject']]['Loadout_Value'] = curr_player_economy['loadoutValue']
                all_players_stats[curr_player_economy['subject']]['Weapon'] = allGuns[curr_player_economy['weapon']]
                all_players_stats[curr_player_economy['subject']]['Armor'] = allArmor[curr_player_economy['armor']]
        else:
            break

        
        #time to pull out data
        if round_result['playerStats'] is not None and isinstance(round_result['playerStats'], list):
            for player_stat in round_result['playerStats']:

                if player_stat['kills'] is not None and isinstance(player_stat['kills'], list):
                    for curr_kill in player_stat['kills']:
                        dbug_print("\t\t\tProcessing new kill/death in round [", round_count, "]")
                        #put in DEATH INFO
                        
                        #GET RID OF STUPID ISO ULT DATA
                        if abs(curr_kill['victimLocation']['x']) > 20000 or abs(curr_kill['victimLocation']['y']) > 20000:
                            continue

                        #calculate where we put datapoint
                        array_spot = (int)(all_players_stats[curr_kill['victim']]['Loadout_Value']/50)
                    
                        dbug_print('\t\t\t\tINSERTING death INTO SLOT: [', array_spot, "]")

                        #add datapoint to output
                        output_dict[map_name][all_players_stats[curr_kill['victim']]['Side']]['death_info'][array_spot].append( {
                        
                            'Location': {'x': curr_kill['victimLocation']['x'], 'y':curr_kill['victimLocation']['y']},
                            'Armor' : all_players_stats[curr_kill['victim']]['Armor']

                        })

                        #put in KILL INFO
                        array_spot = (int)(all_players_stats[curr_kill['killer']]['Loadout_Value']/50)
                    
                        dbug_print('\t\t\t\tINSERTING kill INTO SLOT: [', array_spot, "]")

                        #in case killer location is not found, we skip this(killer location not found is actually possible to happen!)
                        for item in curr_kill['playerLocations']:
                            if item['subject'] == curr_kill['killer']:
                                killer_location = item
                                break
                        else:
                            continue

                        #GET RID OF STUPID ISO ULT DATA
                        if abs(killer_location['location']['x']) > 20000 or abs(killer_location['location']['y']) > 20000:
                            continue

                        output_dict[map_name][all_players_stats[curr_kill['killer']]['Side']]['kill_info'][array_spot].append({
                        
                            'Location': {'x': killer_location['location']['x'], 'y':killer_location['location']['y']},
                            'ViewRadians' : killer_location['viewRadians'],
                            'Weapon' : all_players_stats[curr_kill['killer']]['Weapon']

                        })
                else:
                    continue         
        else:
            break
        

#Does not access API
#auxillary function for get_all_location_data
#given match details (format: https://valapidocs.techchrism.me/endpoint/match-details)
#mutates output_dict by placing new data inside
def analyze_match(curr_match: dict, puuid: str, output_dict: dict):
    

    map_id = curr_match['matchInfo']['mapId']
    map_name = allMaps[map_id]

    analyze_all_players = puuid == ""

    print(f"----CURRENT MAP: [{map_name}]----")

    if map_name not in output_dict:
        if(analyze_all_players):
            output_dict[map_name] = {
                
                'num_matches': 0, #number of matches analyzed for this specific map

               #No kill/death times for allplayers
                "Attack": {
                    #make these all linkedlists which apparently is using deque()
                    "kill_info": [[] for _ in range(160)],
                    "death_info": [[] for _ in range(160)]
                    #WE ARE DITCHING THE PLANT INFO!, making a separate dictionary that gets ALL plant data and defuse data(not just specific player)
                },
                "Defense": {
                    "kill_info": [[] for _ in range(160)],
                    "death_info": [[] for _ in range(160)]
                }
            }
        else:
            output_dict[map_name] = {

                'num_matches': 0, #number of matches analyzed for this specific map

                'All_Kill_Times' : [0]*101, #indexes 0 thru 100 = 101 elements (these are % numbers)
                'All_Death_Times': [0]*101,

                "Attack": {
                    #make these all linkedlists which apparently is using deque()
                    "kill_info": [[] for _ in range(160)],
                    "death_info": [[] for _ in range(160)],
                    #WE ARE DITCHING THE PLANT INFO!, making a separate dictionary that gets ALL plant data and defuse data(not just specific player)
                },
                "Defense": {
                    "kill_info": [[] for _ in range(160)],
                    "death_info": [[] for _ in range(160)]
                }
            }

    output_dict[map_name]['num_matches'] += 1 #add one match to the num matches analyzed

    if(analyze_all_players):
        
        get_data_for_all_players(curr_match, map_name, output_dict)
    else:
        get_data_for_player(curr_match, map_name, puuid, output_dict)
    
    return output_dict


#Accesses API(indirectly)
#returns specified(puuid) player's data 
#data structure image link: [to be added]
def get_all_location_data(puuid: str, all_match_ids: [], examined_matches: set = None, to_return_dict:dict = {}):
    print("START!")
    for index, match_id in enumerate(all_match_ids):

        if(examined_matches is not None and match_id in examined_matches):
            continue

        curr_match = get_match_details(match_id, api_key)

        print("\nExamining Match [", index+1, "]")

        to_return_dict = analyze_match(curr_match, puuid, to_return_dict)

        if(examined_matches is not None):
            examined_matches.add(match_id)

    return to_return_dict

#Accesses API(indirectly)
#returns an array of all of the match ids that we have access to (from the api)
def get_player_match_IDs(puuid: str):
    
    match_history: dict = get_raw(puuid, api_key, mode ,0 ,25)

    total_elements = match_history['Total']
    
    history = []

    history.extend([match['MatchID'] for match in match_history['History']])

    if total_elements > 25:#matchhistory: limit = 25 at a time
        for i in range(25, total_elements, 25):
            next_batch = get_raw(puuid, api_key, mode, i, i+25)
            history.extend([match['MatchID'] for match in next_batch['History']])

    return history


#TAKES LOT OF TIME !! !
#creates a dictionary where the keys are puuids, and the values are GEA structures corresponding to each puuid
#Only use this one if you need to distinguish between individual players stats
def get_individual_data_for_players(puuids: list):
    toReturn={}
    for currID in puuids:
        
        toReturn[currID] = get_all_location_data(currID,get_player_match_IDs(currID))

    return toReturn



#UNUSED
#adds multiple players ids to one big GEA structure
def get_all_players_location_data(players_match_data: dict, api_key: str):
    """
    players_match_data: dict with player puuid as keys and list of match IDs as values
    {
        "puuid1": [match_id1, match_id2, ...],
        "puuid2": [match_id1, match_id2, ...],
        ...
    }
    """
    to_return_dict = {}
    for puuid, match_ids in players_match_data.items():
        to_return_dict = process_player_match_history(puuid, match_ids, to_return_dict, api_key)
    return to_return_dict
#UNUSED
#helper for above
def process_player_match_history(puuid: str, match_ids: [], to_return_dict: dict, api_key: str):
    for index, match_id in enumerate(match_ids):
        curr_match = get_match_details(match_id, api_key)
        
        print("\nExamining Match [", index+1, "]")

        to_return_dict = analyze_match(curr_match, puuid, to_return_dict)
    return to_return_dict


#combines multiple GEA structures into one
def combine(data_structures):

    combined = {}

    for data in data_structures:
        # print(json.dumps(data, indent=4))
        for map_name, map_data in data.items():
            if map_name not in combined:
                combined[map_name] = {
                    'num_matches': 0
                }
            combined[map_name]['num_matches'] += map_data['num_matches']

            phase = "Attack"
            phase_data = map_data[phase]
            if phase not in combined[map_name]:
                combined[map_name][phase] = {
                    "kill_info": [[] for _ in range(160)],
                    "death_info": [[] for _ in range(160)]
                }
            
            for i in range(160):

                # print(type(combined))
                # print(type(combined[map_name]))
                # print(type(combined[map_name][phase]))
                # print(type(combined[map_name][phase]["kill_info"]))
                # print((combined[map_name][phase]["kill_info"]))

                # print(type(combined[map_name][phase]["kill_info"][i]))
                # print("a")
                # print(type(phase_data))
                # print(type(phase_data["kill_info"][i]))
                # print(type(phase_data["death_info"][i]))
                # print(type())


                combined[map_name][phase]["kill_info"][i].extend(phase_data["kill_info"][i])
                combined[map_name][phase]["death_info"][i].extend(phase_data["death_info"][i])


            phase = "Defense"
            phase_data = map_data[phase]
            if phase not in combined[map_name]:
                combined[map_name][phase] = {
                    "kill_info": [[] for _ in range(160)],
                    "death_info": [[] for _ in range(160)]
                }
            
            for i in range(160):

                # print(type(combined))
                # print(type(combined[map_name]))
                # print(type(combined[map_name][phase]))
                # print(type(combined[map_name][phase]["kill_info"]))
                # print((combined[map_name][phase]["kill_info"]))

                # print(type(combined[map_name][phase]["kill_info"][i]))
                # print("a")
                # print(type(phase_data))
                # print(type(phase_data["kill_info"][i]))
                # print(type(phase_data["death_info"][i]))
                # print(type())


                combined[map_name][phase]["kill_info"][i].extend(phase_data["kill_info"][i])
                combined[map_name][phase]["death_info"][i].extend(phase_data["death_info"][i])

    return combined
#=================================================================================================================





#============================================================================================================
#creates GEA structure for one player
#PLAYER SPECIFIC
def analyze_individual(name: str, tag:str):

    puuid = get_puuid(name, tag, api_key)['data']['puuid']
    history = get_player_match_IDs(puuid) 

    print(f'   Number of Matches: [{len(history)}]')

    return get_all_location_data(puuid, history) 


#creates a GEA strucutre for every player in allPlayers
# {
# [puuid] -> GEA structure,
# [puuid] -> GEA structure
#}
#PLAYER SPECIFIC
def analyze_group(allPlayers: list):
    allPuuids = []
    for player in allPlayers:
        allPuuids.append(get_puuid(player['name'], player['tag'], api_key)['data']['puuid'])
    
    return get_individual_data_for_players(allPuuids)


#creates one GEA structure for all mathes played by allPlayers
#NOT PLAYER SPECIFIC
def compile_match_data(allPlayers: list):

    #create a big list of match IDS
    allMatchIDs = []
    for player in allPlayers:
        allMatchIDs.extend(get_player_match_IDs(get_puuid(player['name'], player['tag'], api_key)['data']['puuid']))

    print(f'   Number of Matches: [{len(allMatchIDs)}]')

    #keep track of examined matches to avoid duplicates
    examined_matches = set()
    return get_all_location_data("", allMatchIDs, examined_matches)
    


#designated function for dealing with the fixed GEA data
#inputs the file names
def update_fixed_data(allPlayers: list, fixed_data: str, examined_matches: str):
    #read
    # Load the fixed_data file into a dictionary
    if os.path.exists(fixed_data):
        with open(fixed_data, 'r') as file:
            fixed_data_dict = json.load(file)
    else:
        fixed_data_dict = {}

    # Load the examined_matches file into a set
    if os.path.exists(examined_matches):
        with open(examined_matches, 'r') as file:
            examined_matches_set = set(json.load(file))
    else:
        examined_matches_set = set()
    


    #data processing
    allMatchIDs = []
    for player in allPlayers:
        allMatchIDs.extend(get_player_match_IDs(get_puuid(player['name'], player['tag'], api_key)['data']['puuid']))

    print(f'   Number of Matches: [{len(allMatchIDs)}]')

    #keep track of examined matches to avoid duplicates
    fixed_data_dict = get_all_location_data("", allMatchIDs, examined_matches =examined_matches_set, to_return_dict= fixed_data_dict)
    


    #write
    # Save the updated fixed_data_dict to a temporary file and then rename it
    with tempfile.NamedTemporaryFile('w', delete=False) as temp_file:
        json.dump(fixed_data_dict, temp_file, indent=4)
        temp_file_path = temp_file.name
    os.replace(temp_file_path, fixed_data)

    # Save the updated examined_matches_set to a temporary file and then rename it
    with tempfile.NamedTemporaryFile('w', delete=False) as temp_file:
        json.dump(list(examined_matches_set), temp_file, indent=4)
        temp_file_path = temp_file.name
    os.replace(temp_file_path, examined_matches)
#============================================================================================================




#============================================================================================================

#READ THIS
#DATA PLOTTING FUNCTIONS(feel free to collapse)
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from scipy.ndimage import gaussian_filter
import matplotlib.colors as mcolors
from PIL import Image
from sklearn.neighbors import KernelDensity
import math

# Function to convert game coordinates to image coordinates
#auxiliary function
def game_to_image_coords(game_x, game_y, img_width, img_height, x_multiplier, x_scalar_add, y_multiplier, y_scalar_add):
    x = game_y * x_multiplier + x_scalar_add
    y = game_x * y_multiplier + y_scalar_add
    
    # Scale to image dimensions
    x *= img_width
    y = (1-y) * img_height
    return x, y






#plots kill heatmap, death heatmap, and combines them to make a positioning heatmap
def plot_data(all_data: dict, map_name: str, attack_options: dict = None, defense_options: dict = None, scatterplot: bool = False, logscale: bool = False):
    padding = 200

    if map_name not in all_data:
        print(f"No recorded matches on {map_name}.")
        return
    
    #GETTING THE IMAGE
    map_img = Image.open(rf"map_images\{map_name} Map.png")
    map_img = np.array(map_img)  # Convert the image to a NumPy array
    img_height, img_width, _ = map_img.shape  # Get image dimensions


    

    selected_map = all_data[map_name]


    combined_data = {
            'kill': [],
            'death': []
    }
    
    attack = attack_options is not None 
    defense = defense_options is not None 
    if(not attack and not defense):
       print("please select an option ")
       return

    if(attack):
        
        if(attack_options['kills'] != None):
            if 0 <= attack_options['kills']['lower'] <= 159 and 0 <= attack_options['kills']['upper'] <= 159 and attack_options['kills']['lower'] <= attack_options['kills']['upper']:
                for i in range(attack_options['kills']['lower'], attack_options['kills']['upper'] + 1):
                    curr_kill_value = selected_map['Attack']['kill_info'][i]
                    combined_data['kill'].extend(curr_kill_value)

        if(attack_options['deaths'] != None):
            if 0 <= attack_options['deaths']['lower'] <= 159 and 0 <= attack_options['deaths']['upper'] <= 159 and attack_options['deaths']['lower'] <= attack_options['deaths']['upper']:
                for i in range(attack_options['deaths']['lower'], attack_options['deaths']['upper'] + 1):
                    curr_death_value = selected_map['Attack']['death_info'][i]
                    combined_data['death'].extend(curr_death_value)


    if(defense):
        if(defense_options['kills'] != None):
            if 0 <= defense_options['kills']['lower'] <= 159 and 0 <= defense_options['kills']['upper'] <= 159 and defense_options['kills']['lower'] <= defense_options['kills']['upper']:
                for i in range(defense_options['kills']['lower'], defense_options['kills']['upper'] + 1):
                    curr_kill_value = selected_map['Defense']['kill_info'][i]
                    combined_data['kill'].extend(curr_kill_value)

        if(defense_options['deaths'] != None):
            if 0 <= defense_options['deaths']['lower'] <= 159 and 0 <= defense_options['deaths']['upper'] <= 159 and defense_options['deaths']['lower'] <= defense_options['deaths']['upper']:
                for i in range(defense_options['deaths']['lower'], defense_options['deaths']['upper'] + 1):
                    curr_death_value = selected_map['Defense']['death_info'][i]
                    combined_data['death'].extend(curr_death_value)


    bw = 0.06

    # Plot kill data
    if combined_data['kill']:
        x_coords = [loc['Location']['x'] for loc in combined_data['kill'] ]#x,y swapped!!!!
        y_coords = [loc['Location']['y'] for loc in combined_data['kill'] ]

        # Convert game coordinates to image coordinates
        img_coords = [game_to_image_coords(gx, gy, img_width, img_height, mapCoords[map_name]['xMultiplier'], mapCoords[map_name]['xScalar'], mapCoords[map_name]['yMultiplier'], mapCoords[map_name]['yScalar']) for gx, gy in zip(x_coords, y_coords)]
        img_coords = np.array(img_coords)


        # kde = KernelDensity(bandwidth=bw, kernel='gaussian') #NEW KDE FROM SKLEARN
        # kde.fit(img_coords)
        # xgrid = np.linspace(0, img_width, 200)
        # ygrid = np.linspace(0, img_height, 200)
        # Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
        # grid_points = np.vstack([Xgrid.ravel(), Ygrid.ravel()]).T
        # Z_Kill = np.exp(kde.score_samples(grid_points)).reshape(Xgrid.shape)

        kde = gaussian_kde(img_coords.T, bw_method=bw)
        xgrid = np.linspace(0, img_width, 200)
        ygrid = np.linspace(0, img_height, 200)
        Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
        grid_points = np.vstack([Xgrid.ravel(), Ygrid.ravel()]).T
        Z_Kill = kde(grid_points.T).reshape(Xgrid.shape)



        # Create a plot
        fig, ax = plt.subplots(figsize=(8, 8))

        # Display the map layout image with adjustable aspect ratio
        ax.imshow(map_img, extent=(0, img_width, 0, img_height), aspect='auto', alpha=1)

        if(logscale):
            Z_Kill = np.log(Z_Kill+1)  # Adding 1 to avoid log(0)
        # Display the heatmap
        heatmap = ax.imshow( Z_Kill, extent=(0, img_width, 0, img_height), origin='lower', cmap='magma', alpha=0.6, aspect='equal')

        # Plot the points directly on the image
        if(scatterplot):
            ax.scatter(img_coords[:, 0], img_coords[:, 1], color='green', s=25, alpha=0.3)  # Adjust color, size, and alpha as needed

        # Label axes
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')

        # Add a colorbar to serve as a key for the heatmap colors
        cbar = plt.colorbar(heatmap, ax=ax)
        cbar.set_label('Density')
        
        #set title
        if attack and defense:
            plt.title(f'Kill Locations on {map_name} \n On Attack and Defense')
        elif attack:
            plt.title(f'Kill Locations on {map_name} \n On Attack')
        elif defense:
            plt.title(f'Kill Locations on {map_name} \n On Defense')

        # Show the plot
        plt.show()

            
        
            
            # direction = event.get('ViewRadians', 0)
            # dy = np.cos(direction) * 400 #x,y swapped!!!!
            # dx = np.sin(direction) * 400
            # plt.arrow(x, y, dx, dy, color='green', head_width=10, head_length=20, alpha=0.3, linewidth=0.5)
    
    # Plot death data
    if combined_data['death']:
        x_coords = [loc['Location']['x'] for loc in combined_data['death'] ]#x,y swapped!!!!
        y_coords = [loc['Location']['y'] for loc in combined_data['death'] ]
        

        # Convert game coordinates to image coordinates
        img_coords = [game_to_image_coords(gx, gy, img_width, img_height, mapCoords[map_name]['xMultiplier'], mapCoords[map_name]['xScalar'], mapCoords[map_name]['yMultiplier'], mapCoords[map_name]['yScalar']) for gx, gy in zip(x_coords, y_coords)]
        img_coords = np.array(img_coords)


        # kde = KernelDensity(bandwidth=bw, kernel='gaussian') #NEW KDE FROM SKLEARN
        # kde.fit(img_coords)
        # xgrid = np.linspace(0, img_width, 200)
        # ygrid = np.linspace(0, img_height, 200)
        # Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
        # grid_points = np.vstack([Xgrid.ravel(), Ygrid.ravel()]).T
        # Z_Death = np.exp(kde.score_samples(grid_points)).reshape(Xgrid.shape)
        
        kde = gaussian_kde(img_coords.T, bw_method=bw)
        xgrid = np.linspace(0, img_width, 200)
        ygrid = np.linspace(0, img_height, 200)
        Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
        grid_points = np.vstack([Xgrid.ravel(), Ygrid.ravel()]).T
        Z_Death = kde(grid_points.T).reshape(Xgrid.shape)



        # Create a plot
        fig, ax = plt.subplots(figsize=(8, 8))

        # Display the map layout image with adjustable aspect ratio
        ax.imshow(map_img, extent=(0, img_width, 0, img_height), aspect='auto', alpha=1)

        if(logscale):
            Z_Death = np.log(Z_Death+1)  
        # Display the heatmap
        heatmap = ax.imshow( Z_Death, extent=(0, img_width, 0, img_height), origin='lower', cmap='magma', alpha=0.6, aspect='equal')

        # Plot the points directly on the image
        if(scatterplot):
            ax.scatter(img_coords[:, 0], img_coords[:, 1], color='red', s=25, alpha=0.3)  # Adjust color, size, and alpha as needed

        # Label axes
        ax.set_xlabel('X Coordinate')
        ax.set_ylabel('Y Coordinate')

        # Add a colorbar to serve as a key for the heatmap colors
        cbar = plt.colorbar(heatmap, ax=ax)
        cbar.set_label('Density')
        
        
        #set title
        if attack and defense:
            plt.title(f'Death Locations on {map_name} \n On Attack and Defense')
        elif attack:
            plt.title(f'Death Locations on {map_name} \n On Attack')
        elif defense:
            plt.title(f'Death Locations on {map_name} \n On Defense')

        # Show the plot
        plt.show()


    # Compute the difference between the two KDEs and apply log scale
    # Compute the difference between the two KDEs
    # Z_diff = Z_Kill - Z_Death 
    # Z_diff = np.where(np.abs(Z_diff) < 0.15, 0, Z_diff)
    # Z_diff = Z_diff/(Z_Kill+Z_Death + 10000)

    # Z_Kill = np.where(Z_Kill < 1, 0, Z_Kill)
    # Z_Death = np.where(Z_Death < 1, 0, Z_Death)
    Z_diff = ((Z_Kill + 1) / (Z_Death + 1))#*(Z_Kill + Z_Death)*(1000)

    Z_diff = gaussian_filter(Z_diff, sigma=4)

    # Create a custom colormap with a nonlinear transition to white
    colors = [(0, 'white'), (0.175, 'red'), (0.49,"black"),(0.51,"black"),(0.815, 'green'), (1, 'white')]
    cmap_diff = mcolors.LinearSegmentedColormap.from_list('custom_bwr', colors)


    # Create a plot
    fig, ax = plt.subplots(figsize=(8, 8))

    # Display the map layout image with adjustable aspect ratio
    ax.imshow(map_img, extent=(0, img_width, 0, img_height), aspect='auto', alpha=0.5)

    # Display the heatmap
    heatmap = ax.imshow( Z_diff, extent=(0, img_width, 0, img_height), origin='lower', cmap=cmap_diff, alpha=0.6, aspect='equal', vmin=Z_diff.min(), vmax=Z_diff.max())
    
    #Display the heatmap ORIGINAL
    # heatmap = ax.imshow( Z_diff, extent=(0, img_width, 0, img_height), origin='lower', cmap=cmap_diff, alpha=0.6, aspect='equal', vmin=-np.abs(Z_diff).max(), vmax=np.abs(Z_diff).max())

#SAVED THIS FOR SETTINGS
    # plt.imshow(Z_diff_log, cmap=cmap_diff, origin='lower', extent=[x_min, x_max, y_min, y_max], vmin=-np.abs(Z_diff_log).max(), vmax=np.abs(Z_diff_log).max(), alpha = 0.65)
    
    # Add a colorbar to serve as a key for the heatmap colors
    cbar = plt.colorbar(heatmap, ax=ax)
    cbar.set_label('<--Bad     Good-->')
    
    #set title
    if attack and defense:
        plt.title(f'Positioning Guide on {map_name} \n On Attack and Defense')
    elif attack:
        plt.title(f'Positioning Guide on {map_name} \n On Attack')
    elif defense:
        plt.title(f'Positioning Guide on {map_name} \n On Defense')


    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()


    # plt.title(f"Game Events Visualization on {map_name}")
    # plt.xlabel('Y Coordinate')#x,y swapped!!!!
    # plt.ylabel('X Coordinate')
    # plt.grid(True)
    
    # # Add a legend to explain color codes
    # plt.scatter([], [], color='green', label='Kill Locations', alpha=0.3, s=50)
    # plt.scatter([], [], color='red', label='Death Locations', alpha=0.3, s=50)
    # plt.legend(loc='upper right')

    # plt.show()


#combines the kill and death data to generate a general 'activity' heatmap
def plot_activity(all_data: dict, map_name: str, attack_options: dict = None, defense_options: dict = None, scatterplot: bool = False, logscale: bool = False):
    
    if map_name not in all_data:
        print(f"No recorded matches on {map_name}.")
        return
    
    #GETTING THE IMAGE
    map_img = Image.open(rf"map_images\{map_name} Map.png")
    map_img = np.array(map_img)  # Convert the image to a NumPy array
    img_height, img_width, _ = map_img.shape  # Get image dimensions


 
    selected_map = all_data[map_name]


    combined_data= []
    attack = attack_options is not None  #check which options we want
    defense = defense_options is not None 
    if(not attack and not defense):
       print("please select an option ")
       return

    if(attack):
        if(attack_options['kills'] != None):
            if 0 <= attack_options['kills']['lower'] <= 159 and 0 <= attack_options['kills']['upper'] <= 159 and attack_options['kills']['lower'] <= attack_options['kills']['upper']:
                for i in range(attack_options['kills']['lower'], attack_options['kills']['upper'] + 1):
                    curr_kill_value = selected_map['Attack']['kill_info'][i]
                    combined_data.extend(curr_kill_value)

        if(attack_options['deaths'] != None):
            if 0 <= attack_options['deaths']['lower'] <= 159 and 0 <= attack_options['deaths']['upper'] <= 159 and attack_options['deaths']['lower'] <= attack_options['deaths']['upper']:
                for i in range(attack_options['deaths']['lower'], attack_options['deaths']['upper'] + 1):
                    curr_death_value = selected_map['Attack']['death_info'][i]
                    combined_data.extend(curr_death_value)


    if(defense):
        if(defense_options['kills'] != None):
            if 0 <= defense_options['kills']['lower'] <= 159 and 0 <= defense_options['kills']['upper'] <= 159 and defense_options['kills']['lower'] <= defense_options['kills']['upper']:
                for i in range(defense_options['kills']['lower'], defense_options['kills']['upper'] + 1):
                    curr_kill_value = selected_map['Defense']['kill_info'][i]
                    combined_data.extend(curr_kill_value)

        if(defense_options['deaths'] != None):
            if 0 <= defense_options['deaths']['lower'] <= 159 and 0 <= defense_options['deaths']['upper'] <= 159 and defense_options['deaths']['lower'] <= defense_options['deaths']['upper']:
                for i in range(defense_options['deaths']['lower'], defense_options['deaths']['upper'] + 1):
                    curr_death_value = selected_map['Defense']['death_info'][i]
                    combined_data.extend(curr_death_value)


    
    x_coords = [loc['Location']['x'] for loc in combined_data ]
    y_coords = [loc['Location']['y'] for loc in combined_data ]

    # Convert game coordinates to image coordinates
    img_coords = [game_to_image_coords(gx, gy, img_width, img_height, mapCoords[map_name]['xMultiplier'], mapCoords[map_name]['xScalar'], mapCoords[map_name]['yMultiplier'], mapCoords[map_name]['yScalar']) for gx, gy in zip(x_coords, y_coords)]
    img_coords = np.array(img_coords)


    kde = KernelDensity(bandwidth=12, kernel='gaussian') #NEW KDE FROM SKLEARN
    kde.fit(img_coords)
    xgrid = np.linspace(0, img_width, 200)
    ygrid = np.linspace(0, img_height, 200)
    Xgrid, Ygrid = np.meshgrid(xgrid, ygrid)
    grid_points = np.vstack([Xgrid.ravel(), Ygrid.ravel()]).T
    Z = np.exp(kde.score_samples(grid_points)).reshape(Xgrid.shape)

    # Create a plot
    fig, ax = plt.subplots(figsize=(8, 8))

    # Display the map layout image with adjustable aspect ratio
    ax.imshow(map_img, extent=(0, img_width, 0, img_height), aspect='auto', alpha=1)

    if(logscale):
        Z = np.log(Z+ 0.000004)  # Adding 1 to avoid log(0)
    # Display the heatmap
    heatmap = ax.imshow( Z, extent=(0, img_width, 0, img_height), origin='lower', cmap='magma', alpha=0.6, aspect='equal')

    # Plot the points directly on the image
    if(scatterplot):
        ax.scatter(img_coords[:, 0], img_coords[:, 1], color='blue', s=10, alpha=0.4)  # Adjust color, size, and alpha as needed

    # Label axes
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')

    # Add a colorbar to serve as a key for the heatmap colors
    cbar = plt.colorbar(heatmap, ax=ax)
    cbar.set_label('Density')
    
    if attack and defense:
        plt.title(f'Kills & Death Locations on {map_name} \n On Attack and Defense')
    elif attack:
        plt.title(f'Kills & Death Locations on {map_name} \n On Attack')
    elif defense:
        plt.title(f'Kills & Death Locations on {map_name} \n On Defense')

    # Show the plot
    plt.show()






    # Plot the scatter plot of points
    
    # plt.figure(figsize=(18, 8))
    # if(True):
    #     plt.subplot(1, 2, 1)
    #     plt.scatter(x_coords, y_coords, c='blue', alpha=0.3, s=30)  # Reduced size to half
        
        


    #     plt.title('All Locations')
    #     plt.xlabel('X coordinate')
    #     plt.ylabel('Y coordinate')
    #     plt.imshow(map_img, extent=[x_min-700, x_max+900, y_min-1500, y_max+1950], aspect='auto', alpha=1)

    #     # Plot the KDE contour map
    #     plt.subplot(1, 2, 2)
    #     contour = plt.contourf(X, Y, Z_Kill, levels=10, cmap='magma')  # Adjust levels as needed
    #     plt.colorbar(contour)
    #     plt.title('Topographical Heatmap with KDE')
    #     plt.xlabel('X coordinate')
    #     plt.ylabel('Y coordinate')
    #     plt.show()



    # # Apply logarithmic scaling to enhance contrast
    # Z1_log = np.log(Z_Kill+ 0.00000004)  # Adding 1 to avoid log(0)
    # #plt.contourf(X, Y, Z1_log, levels=10, cmap='magma')  # Adjust levels as needed
    
    # plt.imshow(map_img, extent=[x_min-700, x_max+900, y_min-1500, y_max+1950], aspect='auto', alpha=1)

    # plt.imshow(Z1_log, cmap='magma', origin='lower', extent=[x_min, x_max, y_min, y_max], alpha = 0.65)


    # #plt.imshow(Z1_log, cmap='magma', origin='lower', extent=[x_min+ 3*padding, x_max+ 3*padding, y_min+ 3*padding, y_max+ 3*padding])
    # plt.colorbar(label='Log Density')
    # plt.title('Logarithmic Scale Heatmap of KDE(Kills + Deaths)')
    # plt.xlabel('X coordinate')
    # plt.ylabel('Y coordinate')

    # plt.tight_layout()
    # plt.gca().set_aspect('equal', adjustable='box')
    # plt.show()


#plots all data for all maps in a standard way(coordinate points)
def plot_all_data(all_data):
    combined_data_by_map = {}

    # Combine all data into one dictionary
    for map_name, sides in all_data.items():

        
        
        combined_data_by_map[map_name] = {
            'kill': [kill for side in sides.values() for kills in side.get('kill_info', []) for kill in kills ],
            'death': [death for side in sides.values() for deaths in side.get('death_info', []) for death in deaths ]
        }

    # Plotting the data
    for map_name, data in combined_data_by_map.items():
        plt.figure(figsize=(10, 8))

        

        
        # Plot kill data
        for event in data['kill']:
            if 'Location' in event and event['Location']:
                y = event['Location']['x'] 
                x = event['Location']['y']
                plt.scatter(x, y, marker='o', color='green', alpha=0.3, s=15)  # Reduced size to half
                direction = event.get('ViewRadians', 0)
                dx = np.cos(direction) * 400
                dy = np.sin(direction) * 400
                plt.arrow(x, y, dx, dy, color='green', head_width=10, head_length=20, alpha=0.3, linewidth=0.5)
        
        # Plot death data
        if data['death']:
            y_coords = [loc['Location']['x'] for loc in data['death'] ]
            x_coords = [loc['Location']['y'] for loc in data['death'] ]
            plt.scatter(x_coords, y_coords, c='red', alpha=0.3, s=15)  # Reduced size to half

        plt.title(f"Game Events Visualization on {map_name}")
        plt.xlabel('Y Coordinate')
        plt.ylabel('X Coordinate')
        plt.grid(True)
        
        # Add a legend to explain color codes
        plt.scatter([], [], color='green', label='Kill Locations', alpha=0.3, s=50)
        plt.scatter([], [], color='red', label='Death Locations', alpha=0.3, s=50)
        plt.legend(loc='upper right')

        plt.show()


def plot_buy_frequency(all_data: dict, map_name: str):
    if map_name not in all_data:
        print(f"No recorded matches on {map_name}.")
        return
    
    selected_map = all_data[map_name]
    attack_buy_freq = [0] * 160
    defense_buy_freq = [0] * 160

    for i, (kill_info, death_info) in enumerate(zip(selected_map['Attack']['kill_info'], selected_map['Attack']['death_info'])):
        attack_buy_freq[i] += len(kill_info) + len(death_info)

    for i, (kill_info, death_info) in enumerate(zip(selected_map['Defense']['kill_info'], selected_map['Defense']['death_info'])):
        defense_buy_freq[i] += len(kill_info) + len(death_info)
    plt.figure(figsize=(10, 8))
    plt.subplot(2, 1, 1)
    plt.bar([i * 50 for i in range(len(attack_buy_freq))], attack_buy_freq, alpha=0.5, color='red', label='Attack')
    plt.title(f'Attack Buy Frequency on {map_name}')
    plt.xlabel('Index')
    plt.ylabel('Frequency')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.bar([i * 50 for i in range(len(defense_buy_freq))], defense_buy_freq, alpha=0.5, label='Defense')
    plt.title(f'Defense Buy Frequency on {map_name}')
    plt.xlabel('Index')
    plt.ylabel('Frequency')
    plt.legend()

    plt.tight_layout()
    plt.show()






