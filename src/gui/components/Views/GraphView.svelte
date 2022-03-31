<script type="ts">
  import { afterUpdate } from "svelte";
  import Chart from "chart.js/auto";
  import VideoDataStore from "../../stores/VideoDataStore";

  export let x: any[];
  export let y: any[];

  let ctx;
  let myChart: Chart;

  afterUpdate(async () => {
    console.log(x);
    console.log(y);
    
    if (myChart) myChart.destroy();
    myChart = new Chart(ctx, {
      type: "line",
      data: {
        labels: x,
        datasets: [
          {
            label: "# droplet count",
            data: y,
            backgroundColor: "rgba(255, 99, 132, 0.2)",
            borderColor: "rgba(255, 99, 132, 1)",
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  });
</script>

<canvas id="myChart" width="8" height="4.5" bind:this={ctx} />
