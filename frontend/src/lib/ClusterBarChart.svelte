<script lang="ts">
  import { onDestroy } from 'svelte';
  import Chart from 'chart.js/auto';

  export let data: Record<string, number>;

  let canvas: HTMLCanvasElement;
  let chart: Chart;

  $: if (canvas && data) {
    if (chart) {
      chart.destroy();
    }

    chart = new Chart(canvas, {
      type: 'bar',
      data: {
        labels: Object.keys(data),
        datasets: [{
          label: 'Users per Cluster',
          data: Object.values(data),
          backgroundColor: 'rgba(99, 102, 241, 0.7)',
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false
          }
        }
      }
    });
  }

  onDestroy(() => {
    if (chart) {
      chart.destroy();
    }
  });
</script>

<canvas bind:this={canvas}></canvas>
