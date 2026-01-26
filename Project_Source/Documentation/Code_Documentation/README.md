# Open Viatica Developer Documentation

Ok, is everyone else gone? Just you and me?
<br>
All right, lets get technical.
<br><br>
Look, I like to document a lot of things with diagrams, so most of it is going to be like that.
<br>
If the diagrams are not up to standard I am just going to blame it on my bad mermaid skills
<br><br>
Although the purpose of most of these diagrams are to show what features and things the program will do, it could become the main navigation tool for the code, idk.
<br>
It might make it harder to document a full list if features for tracking and the like but its what really makes sense to me, so lets start.
<br><br>
NOTE: ALL clickable diagrams has to be flowchart unless someone can show me a way to do it while meeting my diagram requirements. (PS I´d really prefer ER/Requirement diagrams for a lot of what I am going to document but oh well. I have not found out a way to link them)

# OpenViatica 
## Philosophy & Design
This section will contain all high level the information of the OpenViatica project and it will also contain the Philosophy and design of what the OpenViatica tool is supposed to help with.

1. OpenViatica should be considered something like an engine for the cration and management of a data analysis workspace.

2. The features it implements should directly tie to the creation of a new workspace or the management of an existin one.

3. Whenever there are third party tools that can fulfill the requirements needed to do data analysis work, we will always use that tool. If not, then we will make our own or build on top of it to fulfill the requirements.

4. OpenViatica should be designed to be usable from the smallest data analyst to the largest data analysis companies. This means the tool should easy for begginners but deep for masters.
    1. It will accomplish this goal by being a local-first, but cloud integrated solution for data analytics
5. To accomplish this the features needed for a solo developer analyst to use the tools will be supported on the Windows platform, the other features would be supported in linux only.
<br><br>
OpenViatica is designed to be a local-first but cloud-integrated workspace manager. The idea is that it is easy enough for beginners to ues but deep enough for large cross functional teams in an organization.
<br>
## OpenViatica Interactions Diagram

The purpose of this diagram is to show what the OpenViatica Software does and what interactions are with things that are externally to itself

