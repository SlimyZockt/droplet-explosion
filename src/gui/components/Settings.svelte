<script lang="ts">

    import { Input, ListGroup, ListGroupItem, Button } from "sveltestrap";
    // import {loadWasm} from "../rust/wasm";
    // export const eel = window.eel
    // eel.set_host( 'ws://localhost:8080' )

    $: settings = [
        "color_filtering",
        "edge_detection"
    ];

    $: checked = []


    const handleToggle = (value: number) => {
        const currentIndex = checked.indexOf(value);
        const newChecked = [...checked];

        if (currentIndex === -1) {
        newChecked.push(value);
        } else {
        newChecked.splice(currentIndex, 1);
        }

        checked = newChecked;
        console.log(checked);

        window.electron.update_setting(checked);
    };


</script>

<ListGroup>
    {#each settings as setting, i}
        <ListGroupItem tag="button" action value={i} on:click={() => handleToggle(i)}>
            {setting.replaceAll("_", " ")}
            <Input type="checkbox" checked={checked.indexOf(i) !== -1} on:keypress={() => handleToggle(i)}/>
        </ListGroupItem>
    {/each}
    <ListGroupItem >
        <Button on:click={() => window.electron.update_setting(checked)}>Update Settings</Button>
    </ListGroupItem>
</ListGroup>