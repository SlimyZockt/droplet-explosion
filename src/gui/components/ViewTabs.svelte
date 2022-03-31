<script type="ts">
import { afterUpdate } from "svelte";

  import { TabContent, TabPane } from "sveltestrap";
  import VideoDataStore from "../stores/VideoDataStore";
  import GraphView from "./Views/GraphView.svelte";
  import TableView from "./Views/TableView.svelte";
  import VideoView from "./Views/VideoView.svelte";


  export let video_data: VideoData;


  afterUpdate(() => {
    console.log(video_data);

  })

  // VideoDataStore.subscribe((new_data: VideoData) => {
  //   video_data = new_data;
  //   // data_length = new_data.data.droplet_count.length
  //   console.log(new_data);
  // });
</script>

<TabContent class="max-width" >
  <TabPane tabId="video-view" tab="Video View" active>
    <VideoView />
  </TabPane>
  <TabPane tabId="graph-view" tab="Graph View">
    <GraphView
      x={video_data.data.time_in_s}
      y={video_data.data.droplet_count}
    />
  </TabPane>
  <TabPane tabId="table-view" tab="Table View">
    <TableView data={video_data}/>
  </TabPane>
</TabContent>