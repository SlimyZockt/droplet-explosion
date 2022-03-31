<script lang="ts">
  import VideoPlayer from "svelte-video-player";
  import { Button, Spinner } from "sveltestrap"
  import { Col, Container, Row } from "sveltestrap";
  import { Navbar, NavbarBrand } from "sveltestrap";
  import Settings from "./components/Settings.svelte";
  import PathStore from "./stores/PathStore";
  import ViewTabs from "./components/ViewTabs.svelte";
  import VideoDataStore from "./stores/VideoDataStore";

  let is_loading = false;

  let video_data: VideoData = {
    data: {
    droplet_count: [],
    time_in_s: []
    }
    }

  let data: Promise<any>

  const get_video_path = async () => {
    let files: string
    await fetch("/choose/path",{
      method: "post",
      cache: 'no-cache'
    }).then(data => {
      console.log(data)
      return data.json();
    })
    .then(res => {
      files = res.files
      console.log(files);
    })
    .catch(err => console.log(err))
    // PathStore.set(files)
    // console.log(files)
    // let url = `${files.at(0).replaceAll(' ', '%20').replace(/\\/g, '/')}`;
    // // console.log(url)
    // // console.log(files)
    data = fetch(`/analyse/video`, {
      method: 'post',
      cache: 'no-cache',
      body: JSON.stringify({
        files: files,
        debug: true
      })
    })
    data.then((res) => {
        video_data = res
      console.log(res)
    }
    )
  };

</script>

<main>
  <Container fluid>
    <Row>
      <Col>
		<Navbar color={"dark"} dark>
      <p class="navbar-text">Droplet Explosions</p>
      {#await data}
        <Spinner color={'secondary'} type="border" />
      {:then data}
        <Button class="me-2" on:click={() => get_video_path()}>
          Open File
        </Button>
      {/await}
    </Navbar>
      </Col>
    </Row>
    <Row>
      <Col xs="3">
		    <Settings/>
      </Col>
      <Col class="max-width">
        <ViewTabs {video_data}/>
      </Col>
    </Row>
  </Container>
</main>

