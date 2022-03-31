<script lang="ts">
    import { onMount } from 'svelte';
    import { afterUpdate, dataset_dev } from 'svelte/internal';
    import { Table, Column } from 'sveltestrap';
    import VideoDataStore from '../../stores/VideoDataStore';

    // $: data = new Object();
    export let data: VideoData;

</script>
<Table>
    <thead>
        {#each Object.keys(data.data) as key, _ }
        <th>{key}</th>
        {/each}
        <!-- <th>timestamp</th> -->
    </thead>
    {#key data}
        <tbody>
            {#each Array(data.data.droplet_count.length) as _, i}
            <tr>
                {#each Object.values(data.data) as value, _ }
                <th>{value[i + 1]}</th>
                {/each}
            </tr>
            {/each}
        </tbody>
    {/key}
</Table>
